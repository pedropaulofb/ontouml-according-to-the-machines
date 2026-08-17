#!/usr/bin/env python3
"""Provider observations and failure classification for Phase 2 LLM calls."""

from __future__ import annotations

import json
import os
import re
import tempfile
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Mapping

DEFAULT_QUOTA_COOLDOWN_SECONDS = 3600
DEFAULT_UNAVAILABLE_COOLDOWN_SECONDS = 3600

PROVIDER_POLICY_MARKERS = (
    "provider_error_kind=provider_policy_block",
    "402",
    "billing",
    "payment required",
    "payment method",
    "insufficient credit",
    "insufficient funds",
    "purchase",
    "paygo",
    "pay-as-you-go",
    "paid tier",
    "nonzero price",
    "not proven free",
)
PROVIDER_WIDE_POLICY_MARKERS = (
    "402",
    "billing",
    "payment required",
    "payment method",
    "insufficient credit",
    "insufficient funds",
    "purchase",
    "paygo",
    "pay-as-you-go",
    "paid tier",
)
AUTHENTICATION_MARKERS = (
    "invalid api key",
    "invalid_api_key",
    "incorrect api key",
    "authentication",
    "authorization failed",
    "unauthorized",
    "forbidden",
    "permission_denied",
    "status 401",
    "status 403",
    "http 401",
    "http 403",
    "error code: 401",
    "error code: 403",
    "environment variable is not set",
    "api key environment variable",
    "neither google_api_key",
)
DETERMINISTIC_REQUEST_MARKERS = (
    "provider_error_kind=execution_configuration_block",
    "unsupported parameter",
    "invalid parameter",
    "invalid request",
    "invalid_request_error",
    "invalid_argument",
    "bad request",
    "request too large",
    "context length",
    "maximum context length",
    "status 400",
    "status 413",
    "status 422",
    "http 400",
    "http 413",
    "http 422",
    "error code: 400",
    "error code: 413",
    "error code: 422",
)
NOT_FOUND_MARKERS = (
    "model not found",
    "model_not_found",
    "endpoint not found",
    "not_found",
    "status 404",
    "http 404",
    "error code: 404",
)
QUOTA_MARKERS = (
    "provider_error_kind=rate_or_quota_limited",
    "429",
    "rate_limit",
    "rate limit",
    "resource_exhausted",
    "quota",
    "too many requests",
    "requests per day",
    "requests per minute",
    "tokens per minute",
    "tpm",
    "rpm",
)
TRANSIENT_MARKERS = (
    "provider_error_kind=provider_unavailable",
    "500",
    "502",
    "503",
    "504",
    "service_unavailable",
    "temporarily unavailable",
    "timeout",
    "timed out",
    "connection error",
    "connection reset",
    "too busy",
    "overloaded",
    "capacity",
    "try again later",
    "unavailable",
)


@dataclass(frozen=True)
class FailureClassification:
    """Sanitized provider failure semantics used by quota and task state."""

    kind: str
    scope: str
    quota_group_ids: tuple[str, ...]
    retryable_immediately: bool
    retry_after_seconds: int | None
    retry_not_before: str | None
    retry_source: str
    diagnostic: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def normalize_headers(headers: Mapping[str, Any] | None) -> dict[str, str]:
    if headers is None:
        return {}
    return {str(key).strip().lower(): str(value).strip() for key, value in headers.items()}


def exception_headers(exc: Exception) -> dict[str, str]:
    candidates = [
        getattr(exc, "headers", None),
        getattr(getattr(exc, "response", None), "headers", None),
    ]
    for candidate in candidates:
        if isinstance(candidate, Mapping):
            return normalize_headers(candidate)
        if candidate is not None and hasattr(candidate, "items"):
            try:
                return normalize_headers(dict(candidate.items()))
            except Exception:  # noqa: BLE001 - SDK header containers vary.
                continue
    return {}


def safe_diagnostic(exc: Exception) -> str:
    raw = " ".join(
        str(value)
        for value in (
            exc,
            getattr(exc, "code", ""),
            getattr(exc, "status", ""),
            getattr(exc, "reason", ""),
            getattr(exc, "body", ""),
        )
    )
    sanitized = re.sub(
        r"(?i)([\"']?(?:api[-_ ]?key|authorization|token)[\"']?\s*[:=]\s*)"
        r"(?:[\"'][^\"']*[\"']|(?:bearer\s+)?[^\s,}\]]+)",
        r"\1<redacted>",
        raw,
    )
    sanitized = re.sub(r"\b(?:sk|gsk|AIza)[A-Za-z0-9_-]{12,}\b", "<redacted-credential>", sanitized)
    return " ".join(sanitized.split())[:1000]


def _duration_seconds(value: str) -> int | None:
    normalized = value.strip().lower()
    if not normalized:
        return None
    try:
        return max(0, int(float(normalized)))
    except ValueError:
        pass
    duration_match = re.fullmatch(
        r"(?:(?P<hours>\d+(?:\.\d+)?)h)?(?:(?P<minutes>\d+(?:\.\d+)?)m)?(?:(?P<seconds>\d+(?:\.\d+)?)s)?",
        normalized,
    )
    if duration_match and duration_match.group(0):
        hours = float(duration_match.group("hours") or 0)
        minutes = float(duration_match.group("minutes") or 0)
        seconds = float(duration_match.group("seconds") or 0)
        return max(0, int(hours * 3600 + minutes * 60 + seconds))
    return None


def retry_after_seconds(
    headers: Mapping[str, Any] | None,
    diagnostic: str,
    *,
    now: datetime,
) -> int | None:
    normalized_headers = normalize_headers(headers)
    retry_after = normalized_headers.get("retry-after")
    if retry_after:
        duration = _duration_seconds(retry_after)
        if duration is not None:
            return duration
        try:
            retry_at = parsedate_to_datetime(retry_after).astimezone(timezone.utc)
            return max(0, int((retry_at - now).total_seconds()))
        except (TypeError, ValueError, OverflowError):
            pass
    for header_name in ("x-ratelimit-reset-tokens", "x-ratelimit-reset-requests"):
        reset_value = normalized_headers.get(header_name)
        if reset_value:
            duration = _duration_seconds(reset_value)
            if duration is not None:
                return duration
    retry_match = re.search(r"retry(?:\s+in|delay)?[^0-9]{0,20}(\d+(?:\.\d+)?)\s*s", diagnostic.lower())
    return max(0, int(float(retry_match.group(1)))) if retry_match else None


def quota_groups_for_failure(provider: str, model: str, diagnostic: str) -> tuple[str, ...]:
    normalized = diagnostic.lower()
    if provider == "openrouter":
        return ("openrouter-free-account",)
    if provider == "sambanova":
        if any(marker in normalized for marker in ("account-wide", "account wide", "account quota")):
            return ("sambanova-account",)
        return (f"sambanova:{model}",)
    if provider == "groq":
        if any(marker in normalized for marker in ("organization-wide", "organization wide", "org-wide")):
            return ("groq-organization",)
        return (f"groq:{model}",)
    if provider == "gemini":
        if any(marker in normalized for marker in ("project-wide", "project wide", "project quota")):
            return ("gemini-project",)
        return (f"gemini:{model}",)
    return ()


def classify_provider_failure(
    *,
    provider: str,
    model: str,
    exc: Exception,
    now: datetime | None = None,
) -> FailureClassification:
    observed_at = now or utc_now()
    diagnostic = safe_diagnostic(exc)
    normalized = diagnostic.lower()
    headers = exception_headers(exc)
    parsed_retry_after = retry_after_seconds(headers, diagnostic, now=observed_at)

    if any(marker in normalized for marker in PROVIDER_POLICY_MARKERS):
        scope = "provider" if any(marker in normalized for marker in PROVIDER_WIDE_POLICY_MARKERS) else "slot"
        kind, groups, immediate, default_cooldown = "provider_policy_block", (), False, None
    elif any(marker in normalized for marker in AUTHENTICATION_MARKERS):
        kind, scope, groups, immediate, default_cooldown = (
            "execution_configuration_block",
            "provider",
            (),
            False,
            None,
        )
    elif any(marker in normalized for marker in NOT_FOUND_MARKERS):
        kind, scope, groups, immediate, default_cooldown = (
            "provider_unavailable",
            "slot",
            (),
            False,
            DEFAULT_UNAVAILABLE_COOLDOWN_SECONDS,
        )
    elif any(marker in normalized for marker in DETERMINISTIC_REQUEST_MARKERS):
        kind, scope, groups, immediate, default_cooldown = (
            "execution_configuration_block",
            "slot",
            (),
            False,
            None,
        )
    elif any(marker in normalized for marker in QUOTA_MARKERS):
        kind, scope, groups, immediate, default_cooldown = (
            "rate_or_quota_limited",
            "quota_group",
            quota_groups_for_failure(provider, model, diagnostic),
            False,
            DEFAULT_QUOTA_COOLDOWN_SECONDS,
        )
    elif "empty response" in normalized:
        kind, scope, groups, immediate, default_cooldown = (
            "empty_response",
            "slot",
            (),
            True,
            DEFAULT_UNAVAILABLE_COOLDOWN_SECONDS,
        )
    elif any(marker in normalized for marker in TRANSIENT_MARKERS):
        kind, scope, groups, immediate, default_cooldown = (
            "provider_unavailable",
            "slot",
            (),
            True,
            DEFAULT_UNAVAILABLE_COOLDOWN_SECONDS,
        )
    else:
        kind, scope, groups, immediate, default_cooldown = "unknown_provider_error", "slot", (), False, None

    cooldown = parsed_retry_after if parsed_retry_after is not None else default_cooldown
    retry_not_before = format_timestamp(observed_at + timedelta(seconds=cooldown)) if cooldown is not None else None
    retry_source = (
        "provider-reported" if parsed_retry_after is not None else "inferred" if cooldown is not None else "unknown"
    )
    return FailureClassification(
        kind=kind,
        scope=scope,
        quota_group_ids=groups,
        retryable_immediately=immediate,
        retry_after_seconds=cooldown,
        retry_not_before=retry_not_before,
        retry_source=retry_source,
        diagnostic=diagnostic,
    )


def is_transient_retryable(provider: str, model: str, exc: Exception) -> bool:
    return classify_provider_failure(provider=provider, model=model, exc=exc).retryable_immediately


def extract_usage(response: Any) -> dict[str, int | None]:
    usage = getattr(response, "usage", None)
    if usage is not None:
        prompt_tokens = getattr(usage, "prompt_tokens", None)
        completion_tokens = getattr(usage, "completion_tokens", None)
        total_tokens = getattr(usage, "total_tokens", None)
        completion_details = getattr(usage, "completion_tokens_details", None)
        prompt_details = getattr(usage, "prompt_tokens_details", None)
        reasoning_tokens = getattr(completion_details, "reasoning_tokens", None)
        cached_tokens = getattr(prompt_details, "cached_tokens", None)
    else:
        usage = getattr(response, "usage_metadata", None)
        prompt_tokens = getattr(usage, "prompt_token_count", None) if usage is not None else None
        completion_tokens = getattr(usage, "candidates_token_count", None) if usage is not None else None
        total_tokens = getattr(usage, "total_token_count", None) if usage is not None else None
        reasoning_tokens = getattr(usage, "thoughts_token_count", None) if usage is not None else None
        cached_tokens = getattr(usage, "cached_content_token_count", None) if usage is not None else None

    def normalized_token_count(value: Any) -> int | None:
        return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None

    return {
        "input_tokens": normalized_token_count(prompt_tokens),
        "output_tokens": normalized_token_count(completion_tokens),
        "total_tokens": normalized_token_count(total_tokens),
        "reasoning_tokens": normalized_token_count(reasoning_tokens),
        "cached_tokens": normalized_token_count(cached_tokens),
    }


def _event_directory() -> Path | None:
    configured = os.getenv("PHASE2_QUOTA_EVENT_DIR", "").strip()
    return Path(configured) if configured else None


def record_provider_event(
    *,
    provider: str,
    model: str,
    outcome: str,
    request_sent: bool,
    response: Any | None = None,
    headers: Mapping[str, Any] | None = None,
    failure: FailureClassification | None = None,
    observed_at: datetime | None = None,
) -> Path | None:
    event_directory = _event_directory()
    if event_directory is None:
        return None
    timestamp = observed_at or utc_now()
    event_id = f"{time.time_ns():020d}-{uuid.uuid4()}"
    event = {
        "schema_version": 1,
        "event_id": event_id,
        "observed_at": format_timestamp(timestamp),
        "call_source": os.getenv("PHASE2_CALL_SOURCE", "signal").strip() or "signal",
        "provider": provider,
        "model": model,
        "task_id": os.getenv("PHASE2_TASK_ID", "").strip() or None,
        "outcome": outcome,
        "request_sent": request_sent,
        "headers": normalize_headers(headers),
        "usage": extract_usage(response) if response is not None else extract_usage(None),
        "failure": asdict(failure) if failure is not None else None,
    }
    event_directory.mkdir(parents=True, exist_ok=True)
    target = event_directory / f"{event['observed_at'].replace(':', '')}-{event_id}.json"
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=event_directory,
            prefix=".quota-event-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            json.dump(event, temporary_file, indent=2, sort_keys=True)
            temporary_file.write("\n")
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, target)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return target


def record_provider_failure(
    *,
    provider: str,
    model: str,
    exc: Exception,
    request_sent: bool,
    observed_at: datetime | None = None,
) -> FailureClassification:
    classification = classify_provider_failure(provider=provider, model=model, exc=exc, now=observed_at)
    record_provider_event(
        provider=provider,
        model=model,
        outcome="failure",
        request_sent=request_sent,
        headers=exception_headers(exc),
        failure=classification,
        observed_at=observed_at,
    )
    return classification
