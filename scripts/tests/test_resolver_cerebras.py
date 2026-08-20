"""Regression tests that keep Cerebras out of the active Phase 2 resolver."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "phase-2" / "resolve_signal_issue.py"
MODULE_NAME = "phase_2_resolve_signal_issue_without_cerebras"
SPEC = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load resolver module from {MODULE_PATH}")
resolver = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = resolver
SPEC.loader.exec_module(resolver)


class ResolverProviderTests(unittest.TestCase):
    def test_cli_rejects_cerebras_without_changing_primary_defaults(self) -> None:
        with mock.patch.object(
            sys,
            "argv",
            ["resolve_signal_issue.py", "--repo", "example/repository"],
        ):
            defaults = resolver.parse_args()

        self.assertEqual(defaults.provider, "gemini")
        self.assertEqual(defaults.model, "gemini-3.5-flash")
        self.assertEqual(defaults.max_completion_tokens, 8000)

        with (
            mock.patch.object(
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
                ],
            ),
            self.assertRaises(SystemExit),
        ):
            resolver.parse_args()

    def test_resolver_has_no_cerebras_call_path(self) -> None:
        self.assertFalse(hasattr(resolver, "call_cerebras_json"))
        with self.assertRaisesRegex(resolver.ResolverError, "Unsupported provider"):
            resolver.call_provider(
                "cerebras",
                "gpt-oss-120b",
                "prompt",
                "input",
                6000,
                1,
            )

    def test_workflow_uses_cross_provider_groq_fallback(self) -> None:
        workflow = (
            Path(__file__).resolve().parents[2] / ".github" / "workflows" / "phase-2-signal-resolver.yml"
        ).read_text(encoding="utf-8")

        self.assertIn('default: "gemini"', workflow)
        self.assertIn('default: "gemini-3.5-flash"', workflow)
        self.assertNotIn("CEREBRAS_API_KEY", workflow)
        self.assertNotIn('fallback_provider="cerebras"', workflow)
        self.assertIn('fallback_provider="groq"', workflow)
        self.assertIn('fallback_model="openai/gpt-oss-120b"', workflow)
        self.assertIn('fallback_max_completion_tokens="6000"', workflow)
        self.assertIn(
            'run_resolver "$fallback_provider" "$fallback_model"',
            workflow,
        )
        self.assertIn('if [[ "$provider" != "gemini" ]]; then', workflow)
        self.assertIn("provider_unavailable_issue_number()", workflow)
        self.assertNotIn("Running Cerebras fallback", workflow)
        self.assertIn("PHASE2_RESOLVER_ATTEMPT_EVENT_DIR", workflow)
        self.assertIn("--add data/phase-2/resolver-attempt-state.json", workflow)
        self.assertIn("--resolver-attempt-events", workflow)


if __name__ == "__main__":
    unittest.main()
