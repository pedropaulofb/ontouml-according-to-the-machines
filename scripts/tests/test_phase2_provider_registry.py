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
reasoning_policy = importlib.import_module("reasoning_policy")
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
    "gemini:gemini-2.5-pro",
    "gemini:gemini-2.5-flash-lite",
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
    "gemini:gemini-2.5-flash",
    "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free",
    "openrouter:nvidia/nemotron-3-super-120b-a12b:free",
    "openrouter:google/gemma-4-26b-a4b-it:free",
    "openrouter:google/gemma-4-31b-it:free",
    "openrouter:poolside/laguna-s-2.1:free",
    "openrouter:poolside/laguna-xs-2.1:free",
    "openrouter:inclusionai/ling-3.0-flash:free",
    "openrouter:openai/gpt-oss-20b:free",
    "openrouter:nvidia/nemotron-nano-9b-v2:free",
    "gemini:gemini-3.7-flash",
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

        self.assertEqual(len(configured), 25)
        self.assertEqual([slot.spec for slot in configured], EXPECTED_SPECS)
        self.assertEqual(
            Counter(slot.provider for slot in configured),
            Counter({"sambanova": 6, "groq": 3, "gemini": 7, "openrouter": 9}),
        )
        preview = registry.find("gemini", "gemini-3-flash-preview")
        self.assertIsNotNone(preview)
        self.assertEqual(preview.lifecycle, "preview")
        self.assertTrue(REMOVED_SPECS.isdisjoint(slot.spec for slot in configured))
        self.assertEqual(
            [slot.model for slot in configured if slot.provider == "openrouter" and "laguna" in slot.model],
            ["poolside/laguna-s-2.1:free", "poolside/laguna-xs-2.1:free"],
        )
        replacement = registry.find("gemini", "gemini-3.7-flash")
        self.assertIsNotNone(replacement)
        self.assertEqual(replacement.lifecycle, "stable")
        self.assertEqual(replacement.request_config["thinking_level"], "low")
        self.assertEqual(registry.configuration_version, "phase-2-recalibration-v3")
        self.assertEqual({slot.request_config_version for slot in configured}, {"2"})

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

    def test_provider_specific_unsupported_request_field_is_rejected(self) -> None:
        document = registry_document()
        slots = document["slots"]
        assert isinstance(slots, list)
        slots[0]["request_config"]["reasoning_effort"] = "low"

        with self.assertRaisesRegex(registry_module.RegistryValidationError, "unsupported field"):
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

    def test_retired_gemini_slots_are_not_executable(self) -> None:
        registry = registry_module.load_registry(REGISTRY_PATH)
        for model in ("gemini-2.5-pro", "gemini-2.5-flash-lite"):
            slot = registry.find("gemini", model)
            self.assertIsNotNone(slot)
            self.assertEqual(slot.configuration_status, "retired")
            with self.assertRaisesRegex(registry_module.RegistryValidationError, "is retired"):
                registry_module.require_executable_slot("gemini", model, path=REGISTRY_PATH)

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
            self.assertEqual(
                kwargs["extra_body"],
                {
                    "provider": {"allow_fallbacks": False},
                    "reasoning": {"effort": "minimal", "exclude": True},
                },
            )
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


class ReasoningRequestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = registry_module.load_registry(REGISTRY_PATH)

    def slot(self, provider: str, model: str):
        slot = self.registry.find(provider, model)
        self.assertIsNotNone(slot)
        return slot

    def test_groq_uses_only_supported_reasoning_controls(self) -> None:
        gpt_oss = self.slot("groq", "openai/gpt-oss-120b")
        qwen = self.slot("groq", "qwen/qwen3.6-27b")

        self.assertEqual(
            reasoning_policy.groq_request_kwargs(gpt_oss),
            {"reasoning_effort": "low", "include_reasoning": False},
        )
        self.assertEqual(
            reasoning_policy.groq_request_kwargs(qwen),
            {"reasoning_effort": "none", "include_reasoning": False},
        )

    def test_gemini_config_uses_registry_control_and_excludes_thoughts(self) -> None:
        flash = self.slot("gemini", "gemini-3.7-flash")
        legacy_flash = self.slot("gemini", "gemini-2.5-flash")

        self.assertEqual(
            reasoning_policy.gemini_thinking_kwargs(flash),
            {"thinking_level": "low", "include_thoughts": False},
        )
        self.assertNotIn("temperature", flash.request_config)
        self.assertEqual(
            reasoning_policy.gemini_thinking_kwargs(legacy_flash),
            {"thinking_budget": 0, "include_thoughts": False},
        )

    def test_openrouter_uses_normalized_reasoning_and_excludes_trace(self) -> None:
        low = self.slot("openrouter", "openai/gpt-oss-20b:free")
        none = self.slot("openrouter", "nvidia/nemotron-nano-9b-v2:free")

        self.assertEqual(
            reasoning_policy.openrouter_extra_body(low)["reasoning"],
            {"effort": "low", "exclude": True},
        )
        self.assertEqual(
            reasoning_policy.openrouter_extra_body(none)["reasoning"],
            {"effort": "none", "exclude": True},
        )

    def test_sambanova_does_not_send_unsupported_reasoning_fields(self) -> None:
        minimax = self.slot("sambanova", "MiniMax-M2.7")
        gpt_oss = self.slot("sambanova", "gpt-oss-120b")

        self.assertEqual(reasoning_policy.sambanova_request_kwargs(minimax), {})
        self.assertEqual(reasoning_policy.sambanova_request_kwargs(gpt_oss), {"reasoning_effort": "low"})

    def test_reasoning_trace_is_removed_from_openai_compatible_content(self) -> None:
        content = "<think>private reasoning</think>\n## Check signal report: final"
        self.assertEqual(
            openai_compatible.exclude_reasoning_trace(content),
            "## Check signal report: final",
        )
        self.assertEqual(openai_compatible.exclude_reasoning_trace("<think>unfinished"), "")

    def test_groq_adapter_sends_no_internal_registry_fields(self) -> None:
        slot = self.slot("groq", "openai/gpt-oss-120b")
        response = types.SimpleNamespace(choices=[])
        create = mock.Mock(return_value=response)
        client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create)))

        groq_provider._call_groq_once(
            client=client,
            model=slot.model,
            review_input="input",
            max_completion_tokens=3000,
            request_kwargs=reasoning_policy.groq_request_kwargs(slot),
        )

        sent = create.call_args.kwargs
        self.assertEqual(sent["reasoning_effort"], "low")
        self.assertIs(sent["include_reasoning"], False)
        self.assertNotIn("reasoning", sent)
        self.assertNotIn("allow_paid_service_tier", sent)

    def test_gemini_adapter_builds_only_supported_generation_fields(self) -> None:
        slot = self.slot("gemini", "gemini-3.6-flash")

        with (
            mock.patch.object(
                gemini_provider.types,
                "ThinkingConfig",
                side_effect=lambda **kwargs: {"thinking": kwargs},
                create=True,
            ),
            mock.patch.object(
                gemini_provider.types,
                "GenerateContentConfig",
                side_effect=lambda **kwargs: kwargs,
                create=True,
            ),
        ):
            config = gemini_provider._generation_config(slot=slot, max_completion_tokens=3000)

        self.assertNotIn("temperature", config)
        self.assertEqual(
            config["thinking_config"],
            {"thinking": {"thinking_level": "low", "include_thoughts": False}},
        )

    def test_gemini_candidate_extraction_omits_thought_parts(self) -> None:
        response = types.SimpleNamespace(
            text="private reasoning plus final",
            candidates=[
                types.SimpleNamespace(
                    content=types.SimpleNamespace(
                        parts=[
                            types.SimpleNamespace(text="private reasoning", thought=True),
                            types.SimpleNamespace(text="final report", thought=False),
                        ]
                    )
                )
            ],
        )

        self.assertEqual(gemini_provider._response_text(response), "final report")


if __name__ == "__main__":
    unittest.main()
