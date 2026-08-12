"""Tests for the Phase 2 provider registry and free-only request policy."""

from __future__ import annotations

import copy
import importlib
import json
import os
import subprocess
import sys
import types
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPT_DIR = REPO_ROOT / "scripts" / "phase-2"
if str(PHASE2_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPT_DIR))

free_policy = importlib.import_module("free_policy")
registry_module = importlib.import_module("provider_model_registry")
sys.modules.setdefault("openai", types.SimpleNamespace(OpenAI=object))
sys.modules.setdefault("groq", types.SimpleNamespace(Groq=object))
google_module = types.ModuleType("google")
google_genai_module = types.ModuleType("google.genai")
google_genai_types_module = types.ModuleType("google.genai.types")
google_module.genai = google_genai_module
google_genai_module.types = google_genai_types_module
sys.modules.setdefault("google", google_module)
sys.modules.setdefault("google.genai", google_genai_module)
sys.modules.setdefault("google.genai.types", google_genai_types_module)
openrouter = importlib.import_module("providers.openrouter")
gemini_provider = importlib.import_module("providers.gemini")
groq_provider = importlib.import_module("providers.groq")
openai_compatible = importlib.import_module("providers.openai_compatible")
run_check_agent = importlib.import_module("run_check_agent")
run_check_batch = importlib.import_module("run_check_batch")

REGISTRY_PATH = REPO_ROOT / "config" / "phase-2" / "provider-models.json"
REMOVED_SPECS = {
    "cerebras:gpt-oss-120b",
    "cerebras:zai-glm-4.7",
    "openrouter:poolside/laguna-m.1:free",
    "groq:llama-3.3-70b-versatile",
}
EXPECTED_SPECS = [
    "sambanova:MiniMax-M2.7",
    "sambanova:DeepSeek-V3.1",
    "sambanova:Meta-Llama-3.3-70B-Instruct",
    "sambanova:gpt-oss-120b",
    "sambanova:DeepSeek-V3.2",
    "sambanova:gemma-4-31B-it",
    "groq:openai/gpt-oss-120b",
    "groq:openai/gpt-oss-20b",
    "groq:qwen/qwen3.6-27b",
    "gemini:gemini-3.6-flash",
    "gemini:gemini-3.5-flash",
    "gemini:gemini-3.5-flash-lite",
    "gemini:gemini-3.1-flash-lite",
    "gemini:gemini-3-flash-preview",
    "gemini:gemini-2.5-pro",
    "gemini:gemini-2.5-flash",
    "gemini:gemini-2.5-flash-lite",
    "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free",
    "openrouter:nvidia/nemotron-3-super-120b-a12b:free",
    "openrouter:google/gemma-4-26b-a4b-it:free",
    "openrouter:google/gemma-4-31b-it:free",
    "openrouter:poolside/laguna-s-2.1:free",
    "openrouter:poolside/laguna-xs-2.1:free",
    "openrouter:inclusionai/ling-3.0-flash:free",
    "openrouter:openai/gpt-oss-20b:free",
    "openrouter:nvidia/nemotron-nano-9b-v2:free",
]


def registry_document() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def free_metadata(model: str) -> dict[str, object]:
    return {
        "id": model,
        "pricing": {
            "prompt": "0",
            "completion": "0.0",
            "request": 0,
        },
    }


class ProviderModelRegistryTests(unittest.TestCase):
    def test_exact_expected_configured_slots_load(self) -> None:
        registry = registry_module.load_registry(REGISTRY_PATH)
        configured = registry.configured_slots

        self.assertEqual(len(configured), 26)
        self.assertEqual([slot.spec for slot in configured], EXPECTED_SPECS)
        self.assertEqual(
            Counter(slot.provider for slot in configured),
            Counter({"sambanova": 6, "groq": 3, "gemini": 8, "openrouter": 9}),
        )
        preview = registry.find("gemini", "gemini-3-flash-preview")
        self.assertIsNotNone(preview)
        self.assertEqual(preview.lifecycle, "preview")
        self.assertTrue(REMOVED_SPECS.isdisjoint(slot.spec for slot in configured))
        self.assertEqual(
            [slot.model for slot in configured if slot.provider == "openrouter" and "laguna" in slot.model],
            ["poolside/laguna-s-2.1:free", "poolside/laguna-xs-2.1:free"],
        )

    def test_duplicate_slot_is_rejected(self) -> None:
        document = registry_document()
        slots = document["slots"]
        assert isinstance(slots, list)
        duplicate = copy.deepcopy(slots[0])
        duplicate["slot"] = len(slots) + 1
        slots.append(duplicate)

        with self.assertRaisesRegex(registry_module.RegistryValidationError, "duplicate"):
            registry_module.validate_registry_document(document)

    def test_unsupported_provider_is_rejected(self) -> None:
        document = registry_document()
        slots = document["slots"]
        assert isinstance(slots, list)
        slots[0]["provider"] = "cerebras"

        with self.assertRaisesRegex(registry_module.RegistryValidationError, "unsupported provider"):
            registry_module.validate_registry_document(document)

    def test_missing_request_configuration_is_rejected(self) -> None:
        document = registry_document()
        slots = document["slots"]
        assert isinstance(slots, list)
        del slots[0]["request_config"]

        with self.assertRaisesRegex(registry_module.RegistryValidationError, "request_config"):
            registry_module.validate_registry_document(document)

    def test_non_free_openrouter_identifier_is_rejected(self) -> None:
        document = registry_document()
        slots = document["slots"]
        assert isinstance(slots, list)
        openrouter_slot = next(slot for slot in slots if slot["provider"] == "openrouter")
        openrouter_slot["model"] = "nvidia/nemotron-3-ultra-550b-a55b"

        with self.assertRaisesRegex(registry_module.RegistryValidationError, "exact :free"):
            registry_module.validate_registry_document(document)

    def test_direct_runner_does_not_register_cerebras(self) -> None:
        self.assertNotIn("cerebras", run_check_agent.SUPPORTED_PROVIDERS)
        with self.assertRaisesRegex(registry_module.RegistryValidationError, "Unsupported Phase 2"):
            registry_module.require_executable_slot("cerebras", "gpt-oss-120b", path=REGISTRY_PATH)

    def test_batch_cli_rejects_cerebras(self) -> None:
        with (
            mock.patch.object(
                sys,
                "argv",
                [
                    "run_check_batch.py",
                    "--provider",
                    "cerebras",
                    "--model",
                    "gpt-oss-120b",
                ],
            ),
            self.assertRaises(SystemExit),
        ):
            run_check_batch.parse_args()

    def test_collector_uses_registry_and_has_no_removed_route(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "check-agent-signal-collector.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("provider_model_registry.py list-specs", workflow)
        self.assertIn("provider_model_registry.py validate-specs", workflow)
        self.assertNotIn("CEREBRAS_API_KEY", workflow)
        self.assertNotIn("laguna-m.1", workflow)

    def test_deterministic_request_failure_is_an_execution_configuration_block(self) -> None:
        result = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="ERROR: Provider call failed: invalid request (HTTP 400)",
        )

        classification = run_check_batch.classify_provider_failure(result)

        self.assertIsNotNone(classification)
        self.assertEqual(classification.kind, "execution_configuration_block")
        self.assertFalse(classification.nonfatal_when_allowed)

    def test_purchase_diagnostic_is_a_provider_policy_block(self) -> None:
        error = RuntimeError("Purchase more credits to continue.")

        self.assertEqual(openai_compatible._provider_error_kind(error), "provider_policy_block")
        self.assertEqual(groq_provider._provider_error_kind(error), "provider_policy_block")
        self.assertEqual(gemini_provider._provider_error_kind(error), "provider_policy_block")

        result = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="ERROR: Provider call failed: Purchase more credits to continue.",
        )
        classification = run_check_batch.classify_provider_failure(result)
        self.assertIsNotNone(classification)
        self.assertEqual(classification.kind, "provider_policy_block")
        self.assertFalse(classification.nonfatal_when_allowed)


class OpenRouterFreePolicyTests(unittest.TestCase):
    MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

    def test_nonzero_openrouter_price_is_rejected(self) -> None:
        metadata = free_metadata(self.MODEL)
        pricing = metadata["pricing"]
        assert isinstance(pricing, dict)
        pricing["completion"] = "0.000001"

        with self.assertRaisesRegex(free_policy.FreePolicyError, "completion pricing"):
            free_policy.verify_openrouter_free_model(
                self.MODEL,
                "test-key",
                metadata_loader=lambda _model, _key: metadata,
            )

    def test_nonzero_conditional_price_is_rejected(self) -> None:
        metadata = free_metadata(self.MODEL)
        pricing = metadata["pricing"]
        assert isinstance(pricing, dict)
        pricing["overrides"] = [{"min_prompt_tokens": 1000, "prompt": "0.01"}]

        with self.assertRaisesRegex(free_policy.FreePolicyError, "override 1"):
            free_policy.verify_openrouter_free_model(
                self.MODEL,
                "test-key",
                metadata_loader=lambda _model, _key: metadata,
            )

    def test_preflight_runs_before_completion_and_disables_fallbacks(self) -> None:
        events: list[str] = []

        def preflight(model: str, api_key: str) -> dict[str, object]:
            self.assertEqual(model, self.MODEL)
            self.assertEqual(api_key, "test-key")
            events.append("preflight")
            return free_metadata(model)

        def completion(**kwargs: object) -> str:
            events.append("completion")
            self.assertEqual(kwargs["extra_body"], {"provider": {"allow_fallbacks": False}})
            return "report\n"

        with (
            mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True),
            mock.patch.object(openrouter, "verify_openrouter_free_model", side_effect=preflight),
            mock.patch.object(openrouter, "generate_chat_completion", side_effect=completion),
        ):
            result = openrouter.generate_review(
                review_input="input",
                provider="openrouter",
                model=self.MODEL,
                review_date="2026-08-12",
                page_path="docs/stereotypes/classes/kind.md",
                commit_sha="abc123",
                page_content="page",
                max_completion_tokens=3000,
            )

        self.assertEqual(result, "report\n")
        self.assertEqual(events, ["preflight", "completion"])

    def test_failed_preflight_never_requests_completion(self) -> None:
        with (
            mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True),
            mock.patch.object(
                openrouter,
                "verify_openrouter_free_model",
                side_effect=free_policy.FreePolicyError("price changed"),
            ),
            mock.patch.object(openrouter, "generate_chat_completion") as completion,
        ):
            with self.assertRaisesRegex(openrouter.OpenRouterProviderError, "provider_policy_block"):
                openrouter.generate_review(
                    review_input="input",
                    provider="openrouter",
                    model=self.MODEL,
                    review_date="2026-08-12",
                    page_path="docs/stereotypes/classes/kind.md",
                    commit_sha="abc123",
                    page_content="page",
                    max_completion_tokens=3000,
                )

        completion.assert_not_called()


if __name__ == "__main__":
    unittest.main()
