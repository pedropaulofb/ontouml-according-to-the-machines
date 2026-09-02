#!/usr/bin/env python3
"""Regression tests for Phase 2 provider failure classification and state repair."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_ROOT = REPO_ROOT / "scripts" / "phase-2"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


provider_runtime = load_module("phase2_provider_runtime_regression", PHASE2_ROOT / "provider_runtime.py")
repair_module = load_module(
    "phase2_repair_legacy_provider_blocks_regression",
    PHASE2_ROOT / "repair_legacy_provider_blocks.py",
)


class ProviderFailureClassificationRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 8, 20, 9, 52, 40, tzinfo=timezone.utc)

    def test_gemini_429_quota_outranks_incidental_billing_wording(self) -> None:
        exc = RuntimeError(
            "429 RESOURCE_EXHAUSTED: Quota exceeded for metric "
            "GenerateRequestsPerDayPerProjectPerModel-FreeTier; limit: 20. "
            "See billing details for quota and account information."
        )

        failure = provider_runtime.classify_provider_failure(
            provider="gemini",
            model="gemini-3.5-flash",
            exc=exc,
            now=self.now,
        )

        self.assertEqual(failure.kind, "rate_or_quota_limited")
        self.assertEqual(failure.scope, "quota_group")
        self.assertEqual(failure.quota_group_ids, ("gemini:gemini-3.5-flash",))
        self.assertNotEqual(failure.kind, "provider_policy_block")

    def test_groq_413_request_size_outranks_incidental_billing_url(self) -> None:
        exc = RuntimeError(
            "Error code: 413 - Request too large for model openai/gpt-oss-20b in organization. "
            "TPM limit 8000, requested 8612. Upgrade at https://console.groq.com/settings/billing."
        )

        failure = provider_runtime.classify_provider_failure(
            provider="groq",
            model="openai/gpt-oss-20b",
            exc=exc,
            now=self.now,
        )

        self.assertEqual(failure.kind, "execution_configuration_block")
        self.assertEqual(failure.scope, "slot")
        self.assertEqual(failure.quota_group_ids, ())
        self.assertNotEqual(failure.kind, "provider_policy_block")

    def test_true_billing_only_failure_remains_provider_policy_block(self) -> None:
        failure = provider_runtime.classify_provider_failure(
            provider="groq",
            model="openai/gpt-oss-120b",
            exc=RuntimeError("402 Payment required: billing account has insufficient credit."),
            now=self.now,
        )

        self.assertEqual(failure.kind, "provider_policy_block")
        self.assertEqual(failure.scope, "provider")

    def test_quota_plan_policy_wording_is_not_downgraded_to_transient_quota(self) -> None:
        failure = provider_runtime.classify_provider_failure(
            provider="groq",
            model="openai/gpt-oss-120b",
            exc=RuntimeError("This endpoint requires a paid quota plan; billing must be enabled."),
            now=self.now,
        )

        self.assertEqual(failure.kind, "provider_policy_block")
        self.assertEqual(failure.scope, "provider")

    def test_gemini_server_disconnect_is_provider_unavailable(self) -> None:
        failure = provider_runtime.classify_provider_failure(
            provider="gemini",
            model="gemini-3.5-flash",
            exc=RuntimeError("Server disconnected without sending a response."),
            now=self.now,
        )

        self.assertEqual(failure.kind, "provider_unavailable")
        self.assertEqual(failure.scope, "slot")
        self.assertTrue(failure.retryable_immediately)

    def test_unrelated_provider_exception_remains_unknown(self) -> None:
        failure = provider_runtime.classify_provider_failure(
            provider="gemini",
            model="gemini-3.5-flash",
            exc=RuntimeError("Unexpected response framing failure."),
            now=self.now,
        )

        self.assertEqual(failure.kind, "unknown_provider_error")
        self.assertFalse(failure.retryable_immediately)


class LegacyProviderBlockRepairTests(unittest.TestCase):
    def blocked_runtime(self, slot_id: str, timestamp: str) -> dict[str, object]:
        provider, model = slot_id.split(":", 1)
        return {
            "provider": provider,
            "model": model,
            "status": "blocked_provider_policy",
            "retry_not_before": None,
            "authorized_recheck_task_id": None,
            "block_reason": "provider_policy_block",
            "block_scope": "provider",
            "validation_required": True,
            "last_validation_at": None,
            "last_validation_result": None,
            "last_updated_at": timestamp,
        }

    def blocked_task(self, task_id: str) -> dict[str, object]:
        expected = repair_module.LEGACY_TASK_RECLASSIFICATIONS[task_id]
        return {
            "task_id": task_id,
            "identity": {
                "provider": expected["provider"],
                "model": expected["model"],
            },
            "status": "blocked_provider_policy",
            "updated_at": expected["finished_at"],
            "retry_not_before": expected["retry_not_before"],
            "lease": None,
            "last_outcome": {
                "attempt_id": expected["attempt_id"],
                "finished_at": expected["finished_at"],
                "kind": "provider_policy_block",
                "provider_attempts": 1,
            },
            "result_record": {
                "event_path": expected["event_path"],
            },
        }

    def test_repairs_all_matching_provider_slots_and_preserves_groq_configuration_block(self) -> None:
        gemini_timestamp = repair_module.LEGACY_PROVIDER_POLICY_INCIDENTS["gemini"]
        groq_timestamp = repair_module.LEGACY_PROVIDER_POLICY_INCIDENTS["groq"]
        gemini_slots = {
            "gemini:gemini-3.6-flash",
            "gemini:gemini-3.5-flash",
            "gemini:gemini-3.5-flash-lite",
            "gemini:gemini-3.1-flash-lite",
            "gemini:gemini-3-flash-preview",
            "gemini:gemini-2.5-flash",
        }
        groq_slots = {
            "groq:openai/gpt-oss-120b",
            "groq:openai/gpt-oss-20b",
            "groq:qwen/qwen3.6-27b",
        }
        state = {
            "runtime_slots": {
                **{slot_id: self.blocked_runtime(slot_id, gemini_timestamp) for slot_id in gemini_slots},
                **{slot_id: self.blocked_runtime(slot_id, groq_timestamp) for slot_id in groq_slots},
                "openrouter:example": self.blocked_runtime("openrouter:example", groq_timestamp),
                "gemini:future-model": self.blocked_runtime("gemini:future-model", "2026-08-21T09:52:40Z"),
            }
        }

        repaired = repair_module.repair_legacy_provider_blocks(state)

        expected = gemini_slots | groq_slots
        self.assertEqual(set(repaired), expected)

        for slot_id in expected - {repair_module.GROQ_CONFIGURATION_BLOCK_SLOT}:
            runtime = state["runtime_slots"][slot_id]
            self.assertEqual(runtime["status"], "eligible")
            self.assertIsNone(runtime["retry_not_before"])
            self.assertIsNone(runtime["authorized_recheck_task_id"])
            self.assertIsNone(runtime["block_reason"])
            self.assertIsNone(runtime["block_scope"])
            self.assertFalse(runtime["validation_required"])
            self.assertNotIn("reason", runtime)
            self.assertNotIn("retry_after", runtime)

        groq_runtime = state["runtime_slots"][repair_module.GROQ_CONFIGURATION_BLOCK_SLOT]
        self.assertEqual(groq_runtime["status"], "blocked_execution_configuration")
        self.assertEqual(groq_runtime["block_reason"], "execution_configuration_block")
        self.assertEqual(groq_runtime["block_scope"], "slot")
        self.assertTrue(groq_runtime["validation_required"])
        self.assertIsNone(groq_runtime["retry_not_before"])
        self.assertNotIn("reason", groq_runtime)
        self.assertNotIn("retry_after", groq_runtime)

        self.assertEqual(state["runtime_slots"]["openrouter:example"]["status"], "blocked_provider_policy")
        self.assertEqual(state["runtime_slots"]["gemini:future-model"]["status"], "blocked_provider_policy")

    def test_repair_requires_untouched_legacy_validation_metadata(self) -> None:
        timestamp = repair_module.LEGACY_PROVIDER_POLICY_INCIDENTS["gemini"]
        slot_id = "gemini:gemini-3.5-flash"
        runtime = self.blocked_runtime(slot_id, timestamp)
        runtime["last_validation_at"] = "2026-08-20T12:00:00Z"
        runtime["last_validation_result"] = "failed"
        state = {"runtime_slots": {slot_id: runtime}}

        self.assertEqual(repair_module.repair_legacy_provider_blocks(state), [])
        self.assertEqual(state["runtime_slots"][slot_id]["status"], "blocked_provider_policy")

    def test_repair_is_idempotent(self) -> None:
        timestamp = repair_module.LEGACY_PROVIDER_POLICY_INCIDENTS["gemini"]
        slot_id = "gemini:gemini-3.5-flash"
        state = {"runtime_slots": {slot_id: self.blocked_runtime(slot_id, timestamp)}}

        first = repair_module.repair_legacy_provider_blocks(state)
        second = repair_module.repair_legacy_provider_blocks(state)

        self.assertEqual(first, [slot_id])
        self.assertEqual(second, [])

    def test_clears_only_the_audited_obsolete_recheck_authorization(self) -> None:
        slot_id, task_id = next(iter(repair_module.LEGACY_STALE_RECHECK_AUTHORIZATIONS.items()))
        provider, model = slot_id.split(":", 1)
        state = {
            "runtime_slots": {
                slot_id: {
                    "provider": provider,
                    "model": model,
                    "status": "temporarily_unavailable",
                    "authorized_recheck_task_id": task_id,
                }
            }
        }
        task_state = {
            "tasks": {
                task_id: {
                    "task_id": task_id,
                    "identity": {"provider": provider, "model": model},
                    "status": "obsolete",
                    "lease": None,
                }
            }
        }

        first = repair_module.repair_stale_recheck_authorizations(state, task_state)
        second = repair_module.repair_stale_recheck_authorizations(state, task_state)

        self.assertEqual(first, [slot_id])
        self.assertEqual(second, [])
        self.assertIsNone(state["runtime_slots"][slot_id]["authorized_recheck_task_id"])

    def test_preserves_recheck_authorization_for_a_nonobsolete_task(self) -> None:
        slot_id, task_id = next(iter(repair_module.LEGACY_STALE_RECHECK_AUTHORIZATIONS.items()))
        provider, model = slot_id.split(":", 1)
        state = {
            "runtime_slots": {
                slot_id: {
                    "provider": provider,
                    "model": model,
                    "status": "temporarily_unavailable",
                    "authorized_recheck_task_id": task_id,
                }
            }
        }
        task_state = {
            "tasks": {
                task_id: {
                    "task_id": task_id,
                    "identity": {"provider": provider, "model": model},
                    "status": "pending",
                    "lease": None,
                }
            }
        }

        repaired = repair_module.repair_stale_recheck_authorizations(state, task_state)

        self.assertEqual(repaired, [])
        self.assertEqual(state["runtime_slots"][slot_id]["authorized_recheck_task_id"], task_id)

    def test_repairs_the_two_originating_task_records_to_correct_failure_kinds(self) -> None:
        task_ids = set(repair_module.LEGACY_TASK_RECLASSIFICATIONS)
        task_state = {"tasks": {task_id: self.blocked_task(task_id) for task_id in task_ids}}

        repaired = repair_module.repair_legacy_task_blocks(task_state)

        self.assertEqual(set(repaired), task_ids)
        gemini_task = task_state["tasks"]["088ef7d25755196e92cde50522e43064df9c2084dfad6cd29535269114664b51"]
        self.assertEqual(gemini_task["status"], "deferred_quota")
        self.assertEqual(gemini_task["last_outcome"]["kind"], "rate_or_quota_limited")
        self.assertEqual(gemini_task["retry_not_before"], "2026-08-20T09:52:59Z")

        groq_task = task_state["tasks"]["bb847dfdc9f94805fd2f7a42a36718007a2fbb52fd964797a6fd898061512d1d"]
        self.assertEqual(groq_task["status"], "blocked_execution_configuration")
        self.assertEqual(groq_task["last_outcome"]["kind"], "execution_configuration_block")
        self.assertEqual(groq_task["retry_not_before"], "2026-08-20T09:53:12Z")

    def test_task_repair_requires_exact_legacy_event_signature(self) -> None:
        task_id = "bb847dfdc9f94805fd2f7a42a36718007a2fbb52fd964797a6fd898061512d1d"
        task = self.blocked_task(task_id)
        task["last_outcome"]["attempt_id"] = "later-attempt"
        task_state = {"tasks": {task_id: task}}

        self.assertEqual(repair_module.repair_legacy_task_blocks(task_state), [])
        self.assertEqual(task_state["tasks"][task_id]["status"], "blocked_provider_policy")

    def test_cli_check_does_not_modify_state_file(self) -> None:
        timestamp = repair_module.LEGACY_PROVIDER_POLICY_INCIDENTS["gemini"]
        slot_id = "gemini:gemini-3.5-flash"
        state = {"runtime_slots": {slot_id: self.blocked_runtime(slot_id, timestamp)}}
        with tempfile.TemporaryDirectory() as temporary:
            state_path = Path(temporary) / "quota-state.json"
            task_state_path = Path(temporary) / "task-state.json"
            task_id = "088ef7d25755196e92cde50522e43064df9c2084dfad6cd29535269114664b51"
            task_state = {"tasks": {task_id: self.blocked_task(task_id)}}
            original = json.dumps(state, indent=2, sort_keys=True) + "\n"
            original_tasks = json.dumps(task_state, indent=2, sort_keys=True) + "\n"
            state_path.write_text(original, encoding="utf-8", newline="\n")
            task_state_path.write_text(original_tasks, encoding="utf-8", newline="\n")

            exit_code = repair_module.main(
                [
                    "--state",
                    str(state_path),
                    "--task-state",
                    str(task_state_path),
                    "--check",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(state_path.read_text(encoding="utf-8"), original)
            self.assertEqual(task_state_path.read_text(encoding="utf-8"), original_tasks)


class ResolverWorkflowRegressionTests(unittest.TestCase):
    def test_scheduled_resolver_repairs_state_and_defers_cleanly_on_preflight(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "phase-2-signal-resolver.yml").read_text(encoding="utf-8")

        self.assertIn("Repair legacy provider runtime blocks", workflow)
        self.assertIn("repair_legacy_provider_blocks.py", workflow)
        self.assertIn('--export "data/phase-2/quota-state.json=', workflow)
        self.assertIn("--add data/phase-2/task-state.json", workflow)
        self.assertIn('--export "data/phase-2/task-state.json=', workflow)
        self.assertIn('--task-state "{worktree}/data/phase-2/task-state.json"', workflow)
        self.assertIn('if [[ "$GITHUB_EVENT_NAME" == "schedule" ]]; then', workflow)
        self.assertIn("--preflight-only", workflow)
        self.assertIn("resolver_executable_now", workflow)
        self.assertIn("resolver_capacity_required", workflow)
        self.assertIn("outcome.json", workflow)
        self.assertNotIn("Fallback resolver attempt succeeded", workflow)
        self.assertIn("Scheduled resolver deferred", workflow)
        self.assertIn("| Provider request sent | false |", workflow)
        self.assertIn("| Fallback executable | ${fallback_executable} |", workflow)
        self.assertIn("request_sent=${primary_request_sent}", workflow)
        self.assertIn("preserve_primary_provider_error_artifacts", workflow)

    def test_manual_dry_run_does_not_run_state_repair_writer(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "phase-2-signal-resolver.yml").read_text(encoding="utf-8")

        self.assertIn(
            "if: ${{ github.event_name != 'workflow_dispatch' || github.event.inputs.dry_run != 'true' }}",
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
