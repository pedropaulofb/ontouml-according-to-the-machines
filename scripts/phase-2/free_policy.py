#!/usr/bin/env python3
"""Free-only policy checks for Phase 2 provider requests."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from decimal import Decimal, InvalidOperation
from typing import Any, Callable

OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
REQUIRED_ZERO_PRICE_FIELDS = ("prompt", "completion")
OPTIONAL_ZERO_PRICE_FIELDS = ("request", "internal_reasoning")
POLICY_PRICE_FIELDS = REQUIRED_ZERO_PRICE_FIELDS + OPTIONAL_ZERO_PRICE_FIELDS


class FreePolicyError(RuntimeError):
    """Raised when a request cannot be proven to use only free capacity."""

    def __init__(self, message: str, *, kind: str = "provider_policy_block") -> None:
        self.kind = kind
        super().__init__(f"provider_error_kind={kind}: {message}")


def fetch_openrouter_model_metadata(model: str, api_key: str) -> dict[str, Any]:
    """Fetch exact model metadata from OpenRouter's current model catalogue."""
    request = urllib.request.Request(
        OPENROUTER_MODELS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "ontouml-phase-2-free-policy/1",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:  # noqa: S310 - fixed HTTPS endpoint.
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 402:
            raise FreePolicyError(
                "OpenRouter model metadata requires payment; no completion request was sent."
            ) from exc
        if exc.code in {401, 403}:
            raise FreePolicyError(
                "OpenRouter model metadata authorization failed; no completion request was sent.",
                kind="execution_configuration_block",
            ) from exc
        raise FreePolicyError(
            f"OpenRouter model metadata request failed with HTTP {exc.code}; no completion request was sent.",
            kind="provider_unavailable",
        ) from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FreePolicyError(
            "OpenRouter model metadata could not be read; no completion request was sent.",
            kind="provider_unavailable",
        ) from exc

    models = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(models, list):
        raise FreePolicyError("OpenRouter model metadata response did not contain a model list.")
    exact = [item for item in models if isinstance(item, dict) and item.get("id") == model]
    if len(exact) != 1:
        raise FreePolicyError(f"OpenRouter metadata did not contain the exact configured model ID {model!r}.")
    return exact[0]


def _is_zero_price(value: Any) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    try:
        return Decimal(str(value)) == 0
    except (InvalidOperation, ValueError):
        return False


def _validate_price_object(pricing: Any, *, context: str) -> None:
    if not isinstance(pricing, dict):
        raise FreePolicyError(f"OpenRouter {context} pricing metadata is missing or invalid.")
    for field in REQUIRED_ZERO_PRICE_FIELDS:
        if field not in pricing or not _is_zero_price(pricing[field]):
            raise FreePolicyError(f"OpenRouter {context} {field} pricing is not explicitly zero.")
    for field in OPTIONAL_ZERO_PRICE_FIELDS:
        if field in pricing and not _is_zero_price(pricing[field]):
            raise FreePolicyError(f"OpenRouter {context} {field} pricing is not zero.")


def verify_openrouter_free_model(
    model: str,
    api_key: str,
    *,
    metadata_loader: Callable[[str, str], dict[str, Any]] = fetch_openrouter_model_metadata,
) -> dict[str, Any]:
    """Fail closed unless exact live metadata proves the selected route is free."""
    if not model.endswith(":free"):
        raise FreePolicyError(f"OpenRouter model ID must end in :free: {model!r}.")
    metadata = metadata_loader(model, api_key)
    if metadata.get("id") != model:
        raise FreePolicyError(
            f"OpenRouter metadata resolved to {metadata.get('id')!r}, not the exact configured ID {model!r}."
        )
    _validate_price_object(metadata.get("pricing"), context="base")
    pricing = metadata["pricing"]
    overrides = pricing.get("overrides", [])
    if overrides is None:
        overrides = []
    if not isinstance(overrides, list):
        raise FreePolicyError("OpenRouter pricing overrides metadata is invalid.")
    for index, override in enumerate(overrides, start=1):
        if not isinstance(override, dict):
            raise FreePolicyError(f"OpenRouter pricing override {index} is invalid.")
        for field in POLICY_PRICE_FIELDS:
            if field in override and not _is_zero_price(override[field]):
                raise FreePolicyError(f"OpenRouter pricing override {index} has nonzero {field} pricing.")
    return metadata
