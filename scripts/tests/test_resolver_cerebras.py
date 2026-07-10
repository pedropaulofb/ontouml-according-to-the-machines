"""Regression tests for Cerebras support in the Phase 2 signal resolver."""

from __future__ import annotations

import importlib.util
import os
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "phase-2" / "resolve_signal_issue.py"
MODULE_NAME = "phase_2_resolve_signal_issue_cerebras"
SPEC = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load resolver module from {MODULE_PATH}")
resolver = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = resolver
SPEC.loader.exec_module(resolver)


class _FakeCompletions:
    def __init__(self) -> None:
        self.kwargs: dict[str, object] | None = None

    def create(self, **kwargs: object) -> object:
        self.kwargs = kwargs
        message = types.SimpleNamespace(content='{"overall_decision":"no_accepted_changes"}')
        choice = types.SimpleNamespace(message=message)
        return types.SimpleNamespace(choices=[choice])


class _FakeOpenAI:
    instances: list["_FakeOpenAI"] = []

    def __init__(self, *, api_key: str, base_url: str, max_retries: int) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.max_retries = max_retries
        self.completions = _FakeCompletions()
        self.chat = types.SimpleNamespace(completions=self.completions)
        self.__class__.instances.append(self)


class CerebrasResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        _FakeOpenAI.instances.clear()

    def test_missing_cerebras_api_key_is_reported(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                resolver.ResolverError,
                "CEREBRAS_API_KEY environment variable is not set",
            ):
                resolver.call_cerebras_json("gpt-oss-120b", "input", 6000, 1)

    def test_unsupported_cerebras_model_is_rejected_before_api_call(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"CEREBRAS_API_KEY": "test-key"},
            clear=True,
        ):
            with self.assertRaisesRegex(
                resolver.ResolverError,
                "Unsupported Cerebras resolver model",
            ):
                resolver.call_cerebras_json("zai-glm-4.7", "input", 6000, 1)

    def test_cerebras_call_uses_expected_model_controls_and_json_mode(self) -> None:
        fake_openai_module = types.SimpleNamespace(OpenAI=_FakeOpenAI)
        with (
            mock.patch.dict(
                os.environ,
                {
                    "CEREBRAS_API_KEY": "test-key",
                    "CEREBRAS_BASE_URL": "https://example.invalid/v1",
                },
                clear=True,
            ),
            mock.patch.dict(sys.modules, {"openai": fake_openai_module}),
        ):
            result = resolver.call_cerebras_json(
                "gpt-oss-120b",
                "resolver input",
                6000,
                1,
            )

        self.assertEqual(result, '{"overall_decision":"no_accepted_changes"}\n')
        self.assertEqual(len(_FakeOpenAI.instances), 1)
        client = _FakeOpenAI.instances[0]
        self.assertEqual(client.api_key, "test-key")
        self.assertEqual(client.base_url, "https://example.invalid/v1")
        self.assertEqual(client.max_retries, 0)
        self.assertIsNotNone(client.completions.kwargs)
        request = client.completions.kwargs or {}
        self.assertEqual(request["model"], "gpt-oss-120b")
        self.assertEqual(request["max_completion_tokens"], 6000)
        self.assertEqual(request["reasoning_effort"], "low")
        self.assertEqual(request["temperature"], 0)
        self.assertEqual(request["response_format"], {"type": "json_object"})
        self.assertEqual(
            request["messages"],
            [
                {"role": "system", "content": resolver.JSON_SYSTEM_INSTRUCTION},
                {"role": "user", "content": "resolver input"},
            ],
        )

    def test_call_provider_routes_to_cerebras(self) -> None:
        with mock.patch.object(
            resolver,
            "call_cerebras_json",
            return_value="{}\n",
        ) as call:
            result = resolver.call_provider(
                "cerebras",
                "gpt-oss-120b",
                "prompt",
                "input",
                6000,
                1,
            )

        self.assertEqual(result, "{}\n")
        call.assert_called_once_with(
            "gpt-oss-120b",
            "prompt\n\n## Input\n\ninput",
            6000,
            1,
        )

    def test_cli_accepts_cerebras_without_changing_primary_defaults(self) -> None:
        with mock.patch.object(
            sys,
            "argv",
            ["resolve_signal_issue.py", "--repo", "example/repository"],
        ):
            defaults = resolver.parse_args()

        self.assertEqual(defaults.provider, "gemini")
        self.assertEqual(defaults.model, "gemini-3.5-flash")
        self.assertEqual(defaults.max_completion_tokens, 8000)

        with mock.patch.object(
            sys,
            "argv",
            [
                "resolve_signal_issue.py",
                "--repo",
                "example/repository",
                "--provider",
                "cerebras",
                "--model",
                "gpt-oss-120b",
                "--max-completion-tokens",
                "6000",
            ],
        ):
            cerebras = resolver.parse_args()

        self.assertEqual(cerebras.provider, "cerebras")
        self.assertEqual(cerebras.model, "gpt-oss-120b")
        self.assertEqual(cerebras.max_completion_tokens, 6000)

    def test_workflow_uses_cross_provider_cerebras_fallback(self) -> None:
        workflow = (
            Path(__file__).resolve().parents[2] / ".github" / "workflows" / "phase-2-signal-resolver.yml"
        ).read_text(encoding="utf-8")

        self.assertIn('default: "gemini"', workflow)
        self.assertIn('default: "gemini-3.5-flash"', workflow)
        self.assertIn("CEREBRAS_API_KEY: ${{ secrets.CEREBRAS_API_KEY }}", workflow)
        self.assertIn('fallback_provider="cerebras"', workflow)
        self.assertIn('fallback_model="gpt-oss-120b"', workflow)
        self.assertIn('fallback_max_completion_tokens="6000"', workflow)
        self.assertNotIn("fallback_model:", workflow)
        self.assertNotIn("FALLBACK_MODEL_INPUT", workflow)
        provider_options = workflow.split("options:", 1)[1].split("model:", 1)[0]
        self.assertNotIn("          - cerebras", provider_options)
        self.assertIn(
            'run_resolver "$fallback_provider" "$fallback_model"',
            workflow,
        )
        self.assertNotIn('run_resolver "gemini" "$fallback_model"', workflow)
        self.assertIn('if [[ "$provider" != "gemini" ]]; then', workflow)
        self.assertIn("provider_unavailable_issue_number()", workflow)
        self.assertNotIn("plan-repair", workflow)
        self.assertNotIn("repair-signal-resolution-plan", workflow)


if __name__ == "__main__":
    unittest.main()
