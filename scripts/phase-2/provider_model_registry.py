#!/usr/bin/env python3
"""Load and validate the authoritative Phase 2 provider-model registry."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

DEFAULT_REGISTRY_PATH = Path("config/phase-2/provider-models.json")
EXPECTED_AGENTS = ("page-hygiene-checker", "language-style-checker")
SUPPORTED_PROVIDERS = ("sambanova", "groq", "gemini", "openrouter")
CONFIGURATION_STATUSES = {"configured", "retired"}
EXECUTION_STATUSES = {
    "eligible",
    "temporarily_unavailable",
    "blocked_provider_policy",
    "blocked_execution_configuration",
}
LIFECYCLES = {"production", "preview", "stable", "free-variant"}
FREE_POLICIES = {
    "confirmed-free-account",
    "confirmed-no-charge-project",
    "metadata-verified-zero-price",
}
REMOVED_SPECS = {
    "cerebras:gpt-oss-120b",
    "cerebras:zai-glm-4.7",
    "openrouter:poolside/laguna-m.1:free",
    "groq:llama-3.3-70b-versatile",
}


class RegistryValidationError(ValueError):
    """Raised when the provider-model registry is invalid or inconsistent."""


@dataclass(frozen=True)
class ProviderModelSlot:
    """One validated provider-model configuration slot."""

    slot: int
    provider: str
    model: str
    configuration_status: str
    execution_status: str
    lifecycle: str
    agents: tuple[str, ...]
    quota_groups: tuple[str, ...]
    free_policy: str
    reasoning_policy: str
    output_policy: str
    max_completion_tokens: int
    request_config_version: str
    request_config: dict[str, Any]

    @property
    def spec(self) -> str:
        return f"{self.provider}:{self.model}"

    @property
    def executable(self) -> bool:
        return self.configuration_status == "configured" and self.execution_status == "eligible"


@dataclass(frozen=True)
class ProviderModelRegistry:
    """A fully validated registry document."""

    schema_version: int
    configuration_version: str
    phase: str
    slots: tuple[ProviderModelSlot, ...]

    @property
    def configured_slots(self) -> tuple[ProviderModelSlot, ...]:
        return tuple(slot for slot in self.slots if slot.configuration_status == "configured")

    @property
    def executable_slots(self) -> tuple[ProviderModelSlot, ...]:
        return tuple(slot for slot in self.slots if slot.executable)

    def find(self, provider: str, model: str) -> ProviderModelSlot | None:
        normalized_provider = provider.strip().lower()
        normalized_model = model.strip()
        return next(
            (slot for slot in self.slots if slot.provider == normalized_provider and slot.model == normalized_model),
            None,
        )


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _require_nonempty_string(value: Any, field: str, slot_number: int | None = None) -> str:
    location = f"slot {slot_number} field {field}" if slot_number is not None else f"field {field}"
    if not isinstance(value, str) or not value.strip():
        raise RegistryValidationError(f"Registry {location} must be a non-empty string.")
    if value != value.strip():
        raise RegistryValidationError(f"Registry {location} must not contain leading or trailing whitespace.")
    return value


def _require_string_list(value: Any, field: str, slot_number: int) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise RegistryValidationError(f"Registry slot {slot_number} field {field} must be a non-empty list.")
    normalized = tuple(_require_nonempty_string(item, field, slot_number) for item in value)
    if len(set(normalized)) != len(normalized):
        raise RegistryValidationError(f"Registry slot {slot_number} field {field} contains duplicates.")
    return normalized


def _parse_slot(raw: Any, expected_number: int) -> ProviderModelSlot:
    if not isinstance(raw, dict):
        raise RegistryValidationError(f"Registry slot {expected_number} must be an object.")
    required = {
        "slot",
        "provider",
        "model",
        "configuration_status",
        "execution_status",
        "lifecycle",
        "agents",
        "quota_groups",
        "free_policy",
        "reasoning_policy",
        "output_policy",
        "max_completion_tokens",
        "request_config_version",
        "request_config",
    }
    missing = sorted(required - raw.keys())
    if missing:
        raise RegistryValidationError(
            f"Registry slot {expected_number} is missing required field(s): {', '.join(missing)}."
        )
    unexpected = sorted(raw.keys() - required)
    if unexpected:
        raise RegistryValidationError(
            f"Registry slot {expected_number} has unsupported field(s): {', '.join(unexpected)}."
        )
    if raw["slot"] != expected_number:
        raise RegistryValidationError(
            f"Registry slots must be deterministically ordered and sequential; expected {expected_number}, "
            f"found {raw['slot']!r}."
        )

    provider = _require_nonempty_string(raw["provider"], "provider", expected_number)
    model = _require_nonempty_string(raw["model"], "model", expected_number)
    configuration_status = _require_nonempty_string(
        raw["configuration_status"], "configuration_status", expected_number
    )
    execution_status = _require_nonempty_string(raw["execution_status"], "execution_status", expected_number)
    lifecycle = _require_nonempty_string(raw["lifecycle"], "lifecycle", expected_number)
    agents = _require_string_list(raw["agents"], "agents", expected_number)
    quota_groups = _require_string_list(raw["quota_groups"], "quota_groups", expected_number)
    free_policy = _require_nonempty_string(raw["free_policy"], "free_policy", expected_number)
    reasoning_policy = _require_nonempty_string(raw["reasoning_policy"], "reasoning_policy", expected_number)
    output_policy = _require_nonempty_string(raw["output_policy"], "output_policy", expected_number)
    request_config_version = _require_nonempty_string(
        raw["request_config_version"], "request_config_version", expected_number
    )

    if provider not in SUPPORTED_PROVIDERS:
        raise RegistryValidationError(f"Registry slot {expected_number} uses unsupported provider: {provider}.")
    if configuration_status not in CONFIGURATION_STATUSES:
        raise RegistryValidationError(
            f"Registry slot {expected_number} has unsupported configuration_status: {configuration_status}."
        )
    if execution_status not in EXECUTION_STATUSES:
        raise RegistryValidationError(
            f"Registry slot {expected_number} has unsupported execution_status: {execution_status}."
        )
    if lifecycle not in LIFECYCLES:
        raise RegistryValidationError(f"Registry slot {expected_number} has unsupported lifecycle: {lifecycle}.")
    if agents != EXPECTED_AGENTS:
        raise RegistryValidationError(
            f"Registry slot {expected_number} agents must be exactly: {', '.join(EXPECTED_AGENTS)}."
        )
    if free_policy not in FREE_POLICIES:
        raise RegistryValidationError(f"Registry slot {expected_number} has unsupported free_policy: {free_policy}.")
    if output_policy != "final-only":
        raise RegistryValidationError(f"Registry slot {expected_number} output_policy must be final-only.")
    if not isinstance(raw["max_completion_tokens"], int) or isinstance(raw["max_completion_tokens"], bool):
        raise RegistryValidationError(
            f"Registry slot {expected_number} max_completion_tokens must be a positive integer."
        )
    if raw["max_completion_tokens"] <= 0:
        raise RegistryValidationError(
            f"Registry slot {expected_number} max_completion_tokens must be a positive integer."
        )
    request_config = raw["request_config"]
    if not isinstance(request_config, dict) or not request_config:
        raise RegistryValidationError(f"Registry slot {expected_number} request_config must be a non-empty object.")
    if request_config.get("temperature") != 0:
        raise RegistryValidationError(f"Registry slot {expected_number} request_config.temperature must be 0.")
    if request_config.get("max_completion_tokens") != raw["max_completion_tokens"]:
        raise RegistryValidationError(
            f"Registry slot {expected_number} request_config.max_completion_tokens must match max_completion_tokens."
        )
    if request_config.get("final_output_only") is not True:
        raise RegistryValidationError(f"Registry slot {expected_number} request_config.final_output_only must be true.")
    if provider == "openrouter":
        if not model.endswith(":free"):
            raise RegistryValidationError(
                f"Registry slot {expected_number} OpenRouter model must use an exact :free identifier: {model}."
            )
        if lifecycle != "free-variant":
            raise RegistryValidationError(f"Registry slot {expected_number} OpenRouter lifecycle must be free-variant.")
        if free_policy != "metadata-verified-zero-price":
            raise RegistryValidationError(
                f"Registry slot {expected_number} OpenRouter free_policy must require metadata verification."
            )
        if request_config.get("allow_fallbacks") is not False:
            raise RegistryValidationError(
                f"Registry slot {expected_number} OpenRouter request_config.allow_fallbacks must be false."
            )
    elif provider == "groq" and request_config.get("allow_paid_service_tier") is not False:
        raise RegistryValidationError(
            f"Registry slot {expected_number} Groq request_config.allow_paid_service_tier must be false."
        )
    elif provider == "gemini" and request_config.get("tools") != []:
        raise RegistryValidationError(
            f"Registry slot {expected_number} Gemini request_config.tools must be an empty list."
        )
    elif model.endswith(":free"):
        raise RegistryValidationError(
            f"Registry slot {expected_number} uses an OpenRouter-style :free model outside OpenRouter: {model}."
        )

    return ProviderModelSlot(
        slot=expected_number,
        provider=provider,
        model=model,
        configuration_status=configuration_status,
        execution_status=execution_status,
        lifecycle=lifecycle,
        agents=agents,
        quota_groups=quota_groups,
        free_policy=free_policy,
        reasoning_policy=reasoning_policy,
        output_policy=output_policy,
        max_completion_tokens=raw["max_completion_tokens"],
        request_config_version=request_config_version,
        request_config=request_config,
    )


def validate_registry_document(document: Any) -> ProviderModelRegistry:
    """Validate a decoded registry document and return its normalized representation."""
    if not isinstance(document, dict):
        raise RegistryValidationError("Registry root must be an object.")
    required = {"schema_version", "configuration_version", "phase", "slots"}
    missing = sorted(required - document.keys())
    if missing:
        raise RegistryValidationError(f"Registry root is missing required field(s): {', '.join(missing)}.")
    unexpected = sorted(document.keys() - required)
    if unexpected:
        raise RegistryValidationError(f"Registry root has unsupported field(s): {', '.join(unexpected)}.")
    if document["schema_version"] != 1:
        raise RegistryValidationError("Registry schema_version must be 1.")
    configuration_version = _require_nonempty_string(document["configuration_version"], "configuration_version")
    phase = _require_nonempty_string(document["phase"], "phase")
    if phase != "phase-2":
        raise RegistryValidationError("Registry phase must be phase-2.")
    raw_slots = document["slots"]
    if not isinstance(raw_slots, list) or not raw_slots:
        raise RegistryValidationError("Registry slots must be a non-empty list.")
    slots = tuple(_parse_slot(raw, index) for index, raw in enumerate(raw_slots, start=1))
    specs = [slot.spec for slot in slots]
    duplicates = sorted(spec for spec in set(specs) if specs.count(spec) > 1)
    if duplicates:
        raise RegistryValidationError(f"Registry contains duplicate provider-model slot(s): {', '.join(duplicates)}.")
    active_removed = sorted(
        slot.spec for slot in slots if slot.configuration_status == "configured" and slot.spec in REMOVED_SPECS
    )
    if active_removed:
        raise RegistryValidationError(
            f"Registry configures removed provider-model slot(s): {', '.join(active_removed)}."
        )
    return ProviderModelRegistry(
        schema_version=1,
        configuration_version=configuration_version,
        phase=phase,
        slots=slots,
    )


def load_registry(path: Path | str | None = None) -> ProviderModelRegistry:
    """Load and validate the provider-model registry."""
    registry_path = Path(path) if path is not None else repo_root() / DEFAULT_REGISTRY_PATH
    try:
        document = json.loads(registry_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RegistryValidationError(f"Provider-model registry does not exist: {registry_path}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryValidationError(f"Provider-model registry is not valid JSON: {exc}") from exc
    return validate_registry_document(document)


def configured_provider_model_specs(path: Path | str | None = None) -> tuple[str, ...]:
    return tuple(slot.spec for slot in load_registry(path).configured_slots)


def supported_providers(path: Path | str | None = None) -> tuple[str, ...]:
    return tuple(dict.fromkeys(slot.provider for slot in load_registry(path).configured_slots))


def require_executable_slot(
    provider: str,
    model: str,
    *,
    path: Path | str | None = None,
) -> ProviderModelSlot:
    """Return the exact configured eligible slot or reject the execution request."""
    registry = load_registry(path)
    slot = registry.find(provider, model)
    requested_spec = f"{provider.strip().lower()}:{model.strip()}"
    if slot is None:
        raise RegistryValidationError(
            f"Unsupported Phase 2 provider-model slot: {requested_spec}. Select an exact configured registry slot."
        )
    if slot.configuration_status != "configured":
        raise RegistryValidationError(f"Phase 2 provider-model slot is retired: {slot.spec}.")
    if slot.execution_status != "eligible":
        raise RegistryValidationError(
            f"Phase 2 provider-model slot is not eligible for execution: {slot.spec} "
            f"(execution_status={slot.execution_status})."
        )
    return slot


def validate_completion_token_cap(slot: ProviderModelSlot, requested_tokens: int) -> None:
    """Reject a signal-generation request that exceeds its configured completion cap."""
    if requested_tokens <= 0:
        raise RegistryValidationError("max_completion_tokens must be greater than 0.")
    if requested_tokens > slot.max_completion_tokens:
        raise RegistryValidationError(
            f"Requested max_completion_tokens={requested_tokens} exceeds the configured cap of "
            f"{slot.max_completion_tokens} for {slot.spec}."
        )


def validate_selected_specs(specs: Iterable[str], path: Path | str | None = None) -> tuple[str, ...]:
    """Validate a user-selected registry subset without letting it define new slots."""
    normalized: list[str] = []
    seen: set[str] = set()
    for raw_spec in specs:
        spec = raw_spec.strip()
        if not spec:
            continue
        if ":" not in spec:
            raise RegistryValidationError(f"Invalid provider:model spec without colon: {spec}")
        provider, model = spec.split(":", 1)
        slot = require_executable_slot(provider, model, path=path)
        if slot.spec in seen:
            raise RegistryValidationError(f"Selected provider-model specs contain a duplicate: {slot.spec}.")
        normalized.append(slot.spec)
        seen.add(slot.spec)
    if not normalized:
        raise RegistryValidationError("No usable provider:model specs were provided.")
    return tuple(normalized)


def parse_spec_text(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.replace("\n", ",").split(",") if part.strip())


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and inspect the Phase 2 provider-model registry.")
    parser.add_argument("--registry", default=str(repo_root() / DEFAULT_REGISTRY_PATH))
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate the complete registry.")
    subparsers.add_parser("list-specs", help="Print configured provider:model specs as one comma-separated line.")
    validate_specs = subparsers.add_parser("validate-specs", help="Validate a comma-separated configured subset.")
    validate_specs.add_argument("--specs", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        registry = load_registry(args.registry)
        if args.command == "validate":
            print(
                f"Valid Phase 2 provider-model registry: configuration_version={registry.configuration_version}; "
                f"configured_slots={len(registry.configured_slots)}."
            )
        elif args.command == "list-specs":
            print(",".join(slot.spec for slot in registry.configured_slots))
        elif args.command == "validate-specs":
            print(",".join(validate_selected_specs(parse_spec_text(args.specs), args.registry)))
        else:  # pragma: no cover - argparse limits this branch.
            raise RegistryValidationError(f"Unsupported command: {args.command}")
        return 0
    except (OSError, RegistryValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
