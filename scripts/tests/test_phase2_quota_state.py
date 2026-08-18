"""Tests for Phase 2 quota accounting, cooldowns, and failure isolation."""

from __future__ import annotations

import importlib
import json
import os
import sys
import tempfile
import unittest
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPT_DIR = REPO_ROOT / "scripts" / "phase-2"
if str(PHASE2_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPT_DIR))

provider_runtime = importlib.import_module("provider_runtime")
quota_state = importlib.import_module("quota_state")
registry_module = importlib.import_module("provider_model_registry")
resolver = importlib.import_module("resolve_signal_issue")
batch_runner = importlib.import_module("run_check_batch")
task_identity = importlib.import_module("task_identity")
task_reconciler = importlib.import_module("task_reconciler")
task_state = importlib.import_module("task_state")

REGISTRY_PATH = REPO_ROOT / "config" / "phase-2" / "provider-models.json"
QUOTA_STATE_PATH = REPO_ROOT / "data" / "phase-2" / "quota-state.json"
TIMESTAMP = "2026-08-12T14:00:00Z"
NOW = datetime(2026, 8, 12, 14, 0, tzinfo=timezone.utc)


class HeaderError(RuntimeError):
    def __init__(self, message: str, headers: dict[str, str] | None = None) -> None:
        super().__init__(message)
        self.headers = headers or {}


class QuotaStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = registry_module.load_registry(REGISTRY_PATH)

    def setUp(self) -> None:
        self.state = quota_state.build_initial_state(self.registry, timestamp=TIMESTAMP)

    def event(
        self,
        *,
        event_id: str,
        provider: str,
        model: str,
        observed_at: str = TIMESTAMP,
        call_source: str = "signal",
        outcome: str = "success",
        request_sent: bool = True,
        headers: dict[str, str] | None = None,
        usage: dict[str, int | None] | None = None,
        failure: provider_runtime.FailureClassification | None = None,
        task_id: str | None = None,
    ) -> dict[str, object]:
        return {
            "schema_version": 1,
            "event_id": event_id,
            "observed_at": observed_at,
            "call_source": call_source,
            "provider": provider,
            "model": model,
            "task_id": task_id,
            "outcome": outcome,
            "request_sent": request_sent,
            "headers": headers or {},
            "usage": usage or {"input_tokens": None, "output_tokens": None, "total_tokens": None},
            "failure": asdict(failure) if failure else None,
        }

    def failure(
        self,
        provider: str,
        model: str,
        message: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> provider_runtime.FailureClassification:
        return provider_runtime.classify_provider_failure(
            provider=provider,
            model=model,
            exc=HeaderError(message, headers),
            now=NOW,
        )

    def eligible(
        self,
        state: dict[str, object],
        provider: str,
        model: str,
        *,
        task_id: str | None = None,
        resolver_work_pending: bool = False,
        now: datetime = NOW,
    ) -> bool:
        eligible, _ = quota_state.slot_eligibility(
            state,
            provider=provider,
            model=model,
            task_id=task_id,
            resolver_work_pending=resolver_work_pending,
            now=now,
        )
        return eligible

    def test_checked_in_initial_state_matches_registry(self) -> None:
        state = quota_state.load_state(QUOTA_STATE_PATH, self.registry)
        self.assertEqual(len(state["quota_groups"]), 29)
        self.assertEqual(len(state["runtime_slots"]), 25)
        self.assertIn("gemini:gemini-3.7-flash", state["runtime_slots"])
        self.assertNotIn("gemini:gemini-2.5-pro", state["runtime_slots"])
        self.assertNotIn("gemini:gemini-2.5-flash-lite", state["runtime_slots"])

    def test_sambanova_model_headers_exhaust_only_that_model(self) -> None:
        exhausted = "MiniMax-M2.7"
        other = "DeepSeek-V3.1"
        event = self.event(
            event_id="samba-header",
            provider="sambanova",
            model=exhausted,
            headers={
                "x-ratelimit-limit-requests-day": "10",
                "x-ratelimit-remaining-requests-day": "0",
                "retry-after": "120",
            },
        )
        updated, _ = quota_state.aggregate_events(self.state, [event], self.registry)
        self.assertFalse(self.eligible(updated, "sambanova", exhausted))
        self.assertTrue(self.eligible(updated, "sambanova", other))
        self.assertTrue(self.eligible(updated, "groq", "openai/gpt-oss-20b"))
        self.assertEqual(updated["quota_groups"][f"sambanova:{exhausted}"]["source"], "provider-reported")
        self.assertEqual(updated["quota_groups"]["sambanova-account"]["status"], "eligible")

    def test_sambanova_daily_exhaustion_without_reset_waits_for_next_daily_period(self) -> None:
        model = "MiniMax-M2.7"
        event = self.event(
            event_id="samba-daily-no-reset",
            provider="sambanova",
            model=model,
            headers={
                "x-ratelimit-limit-requests-day": "10",
                "x-ratelimit-remaining-requests-day": "0",
            },
        )
        updated, _ = quota_state.aggregate_events(self.state, [event], self.registry)
        group = updated["quota_groups"][f"sambanova:{model}"]
        self.assertEqual(group["retry_not_before"], "2026-08-13T00:00:00Z")
        self.assertEqual(group["provenance"]["retry_not_before"]["source"], "inferred")

    def test_sambanova_quota_error_is_model_scoped_unless_explicitly_account_wide(self) -> None:
        model = "MiniMax-M2.7"
        model_failure = self.failure("sambanova", model, "429 rate limit exceeded")
        updated, _ = quota_state.aggregate_events(
            self.state,
            [
                self.event(
                    event_id="samba-model",
                    provider="sambanova",
                    model=model,
                    outcome="failure",
                    failure=model_failure,
                )
            ],
            self.registry,
        )
        self.assertFalse(self.eligible(updated, "sambanova", model))
        self.assertTrue(self.eligible(updated, "sambanova", "DeepSeek-V3.1"))

        account_failure = self.failure("sambanova", model, "429 account-wide quota exhausted")
        account_updated, _ = quota_state.aggregate_events(
            self.state,
            [
                self.event(
                    event_id="samba-account",
                    provider="sambanova",
                    model=model,
                    outcome="failure",
                    failure=account_failure,
                )
            ],
            self.registry,
        )
        self.assertFalse(self.eligible(account_updated, "sambanova", model))
        self.assertFalse(self.eligible(account_updated, "sambanova", "DeepSeek-V3.1"))

    def test_openrouter_shared_counter_blocks_all_openrouter_but_not_gemini(self) -> None:
        state = quota_state.build_initial_state(
            self.registry,
            timestamp=TIMESTAMP,
            openrouter_request_limit_day=2,
        )
        events = [
            self.event(
                event_id=f"openrouter-{index}",
                provider="openrouter",
                model=model,
            )
            for index, model in enumerate(
                (
                    "nvidia/nemotron-3-ultra-550b-a55b:free",
                    "google/gemma-4-31b-it:free",
                ),
                start=1,
            )
        ]
        updated, _ = quota_state.aggregate_events(state, events, self.registry)
        self.assertFalse(self.eligible(updated, "openrouter", "nvidia/nemotron-3-ultra-550b-a55b:free"))
        self.assertFalse(self.eligible(updated, "openrouter", "openai/gpt-oss-20b:free"))
        self.assertTrue(self.eligible(updated, "gemini", "gemini-3.5-flash-lite"))
        shared = updated["quota_groups"]["openrouter-free-account"]
        self.assertEqual(shared["requests_used_day_local"], 2)
        self.assertEqual(shared["remaining_estimate"], 0)
        self.assertEqual(shared["source"], "locally-counted")
        self.assertTrue(shared["provenance"]["remaining_estimate"]["estimated"])
        self.assertEqual(shared["provenance"]["remaining_estimate"]["source"], "inferred")

    def test_openrouter_quota_failure_cannot_shorten_known_daily_reset(self) -> None:
        model = "openai/gpt-oss-20b:free"
        account = self.state["quota_groups"]["openrouter-free-account"]
        account["requests_used_day_local"] = 49
        account["remaining_estimate"] = 1
        failure = self.failure("openrouter", model, "429 too many requests")
        updated, _ = quota_state.aggregate_events(
            self.state,
            [
                self.event(
                    event_id="openrouter-final-daily-request",
                    provider="openrouter",
                    model=model,
                    outcome="failure",
                    failure=failure,
                )
            ],
            self.registry,
        )
        account = updated["quota_groups"]["openrouter-free-account"]
        self.assertEqual(account["remaining_estimate"], 0)
        self.assertEqual(account["retry_not_before"], "2026-08-13T00:00:00Z")
        self.assertFalse(
            self.eligible(
                updated,
                "openrouter",
                "google/gemma-4-31b-it:free",
                now=datetime(2026, 8, 12, 16, 0, tzinfo=timezone.utc),
            )
        )

    def test_groq_token_headers_pause_only_the_correct_model_group(self) -> None:
        model = "openai/gpt-oss-20b"
        event = self.event(
            event_id="groq-tokens",
            provider="groq",
            model=model,
            headers={
                "x-ratelimit-limit-tokens": "6000",
                "x-ratelimit-remaining-tokens": "0",
                "x-ratelimit-reset-tokens": "45s",
            },
            usage={"input_tokens": 900, "output_tokens": 100, "total_tokens": 1000},
        )
        updated, _ = quota_state.aggregate_events(self.state, [event], self.registry)
        group = updated["quota_groups"][f"groq:{model}"]
        self.assertEqual(group["tokens_limit_minute"], 6000)
        self.assertEqual(group["tokens_remaining_minute"], 0)
        self.assertEqual(group["total_tokens_used_day_local"], 1000)
        self.assertEqual(group["provenance"]["tokens_remaining_minute"]["source"], "provider-reported")
        self.assertEqual(group["provenance"]["total_tokens_used_day_local"]["source"], "locally-counted")
        self.assertFalse(self.eligible(updated, "groq", model))
        self.assertTrue(self.eligible(updated, "groq", "qwen/qwen3.6-27b"))
        self.assertEqual(updated["quota_groups"]["groq-organization"]["status"], "eligible")

    def test_groq_request_exhaustion_uses_request_reset_not_unexhausted_token_reset(self) -> None:
        model = "openai/gpt-oss-20b"
        event = self.event(
            event_id="groq-request-reset",
            provider="groq",
            model=model,
            headers={
                "x-ratelimit-limit-requests": "1000",
                "x-ratelimit-remaining-requests": "0",
                "x-ratelimit-reset-requests": "30s",
                "x-ratelimit-remaining-tokens": "1000",
                "x-ratelimit-reset-tokens": "10m",
            },
        )
        updated, _ = quota_state.aggregate_events(self.state, [event], self.registry)
        group = updated["quota_groups"][f"groq:{model}"]
        self.assertEqual(group["requests_limit_day"], 1000)
        self.assertIsNone(group["requests_limit_minute"])
        self.assertEqual(group["reset_at"], "2026-08-12T14:00:30Z")
        self.assertEqual(group["retry_not_before"], "2026-08-12T14:00:30Z")

    def test_local_request_decrements_last_provider_reported_daily_remaining_value(self) -> None:
        model = "openai/gpt-oss-20b"
        provider_observation = self.event(
            event_id="groq-provider-remaining",
            provider="groq",
            model=model,
            observed_at="2026-08-12T14:00:00Z",
            headers={
                "x-ratelimit-limit-requests": "100",
                "x-ratelimit-remaining-requests": "90",
            },
        )
        local_only_observation = self.event(
            event_id="groq-local-after-provider",
            provider="groq",
            model=model,
            observed_at="2026-08-12T14:00:01Z",
        )
        updated, _ = quota_state.aggregate_events(
            self.state,
            [provider_observation, local_only_observation],
            self.registry,
        )
        group = updated["quota_groups"][f"groq:{model}"]
        self.assertEqual(group["requests_used_day_local"], 2)
        self.assertEqual(group["remaining_estimate"], 89)
        self.assertEqual(group["provenance"]["remaining_estimate"]["source"], "inferred")

    def test_gemini_unknown_quota_dimension_gets_model_cooldown_and_local_project_counts(self) -> None:
        model = "gemini-3.6-flash"
        failure = self.failure("gemini", model, "RESOURCE_EXHAUSTED: unknown quota dimension")
        event = self.event(
            event_id="gemini-quota",
            provider="gemini",
            model=model,
            outcome="failure",
            failure=failure,
            usage={"input_tokens": 500, "output_tokens": 50, "total_tokens": 550},
        )
        updated, _ = quota_state.aggregate_events(self.state, [event], self.registry)
        model_group = updated["quota_groups"][f"gemini:{model}"]
        project_group = updated["quota_groups"]["gemini-project"]
        self.assertEqual(model_group["retry_not_before"], "2026-08-12T15:00:00Z")
        self.assertEqual(project_group["requests_used_day_local"], 1)
        self.assertEqual(project_group["input_tokens_used_day_local"], 500)
        self.assertTrue(self.eligible(updated, "gemini", "gemini-3.5-flash-lite"))
        self.assertFalse(failure.retryable_immediately)

    def test_retry_after_is_honored(self) -> None:
        failure = self.failure(
            "groq",
            "openai/gpt-oss-20b",
            "429 rate limit",
            headers={"Retry-After": "90"},
        )
        self.assertEqual(failure.retry_after_seconds, 90)
        self.assertEqual(failure.retry_not_before, "2026-08-12T14:01:30Z")
        self.assertFalse(failure.retryable_immediately)
        self.assertFalse(resolver._is_transient_error(HeaderError("429 RESOURCE_EXHAUSTED")))

    def test_preserved_later_cooldown_keeps_original_provenance_timestamp(self) -> None:
        model = "openai/gpt-oss-20b"
        group = self.state["quota_groups"][f"groq:{model}"]
        group["status"] = "deferred_quota"
        group["retry_not_before"] = "2026-08-12T16:00:00Z"
        group["provenance"]["retry_not_before"] = {
            "source": "provider-reported",
            "observed_at": "2026-08-12T13:00:00Z",
            "estimated": False,
        }
        failure = self.failure("groq", model, "429 too many requests")
        updated, _ = quota_state.aggregate_events(
            self.state,
            [
                self.event(
                    event_id="shorter-cooldown",
                    provider="groq",
                    model=model,
                    outcome="failure",
                    request_sent=False,
                    failure=failure,
                )
            ],
            self.registry,
        )
        provenance = updated["quota_groups"][f"groq:{model}"]["provenance"]["retry_not_before"]
        self.assertEqual(provenance["source"], "provider-reported")
        self.assertEqual(provenance["observed_at"], "2026-08-12T13:00:00Z")

    def test_common_sdk_error_shapes_are_classified_by_operational_semantics(self) -> None:
        authentication = self.failure(
            "groq",
            "openai/gpt-oss-20b",
            "Error code: 401 - invalid_api_key",
        )
        missing_model = self.failure(
            "groq",
            "openai/gpt-oss-20b",
            "Error code: 404 - invalid_request_error: model_not_found",
        )
        invalid_request = self.failure(
            "gemini",
            "gemini-3.6-flash",
            "Error code: 400 - INVALID_ARGUMENT",
        )
        self.assertEqual((authentication.kind, authentication.scope), ("execution_configuration_block", "provider"))
        self.assertEqual((missing_model.kind, missing_model.scope), ("provider_unavailable", "slot"))
        self.assertEqual((invalid_request.kind, invalid_request.scope), ("execution_configuration_block", "slot"))
        self.assertFalse(authentication.retryable_immediately)
        self.assertFalse(missing_model.retryable_immediately)
        self.assertFalse(invalid_request.retryable_immediately)

    def test_unavailable_slot_allows_one_recheck_after_cooldown(self) -> None:
        provider = "gemini"
        model = "gemini-3.6-flash"
        failure = self.failure(provider, model, "503 temporarily unavailable")
        updated, _ = quota_state.aggregate_events(
            self.state,
            [self.event(event_id="unavailable", provider=provider, model=model, outcome="failure", failure=failure)],
            self.registry,
        )
        before = datetime(2026, 8, 12, 14, 59, tzinfo=timezone.utc)
        after = datetime(2026, 8, 12, 15, 1, tzinfo=timezone.utc)
        self.assertFalse(self.eligible(updated, provider, model, task_id="task-a", now=before))
        self.assertTrue(
            quota_state.authorize_slot_recheck(
                updated,
                provider=provider,
                model=model,
                task_id="task-a",
                now=after,
            )
        )
        self.assertTrue(self.eligible(updated, provider, model, task_id="task-a", now=after))
        self.assertFalse(self.eligible(updated, provider, model, task_id="task-b", now=after))
        self.assertFalse(
            quota_state.authorize_slot_recheck(
                updated,
                provider=provider,
                model=model,
                task_id="task-b",
                now=after,
            )
        )

    def test_successful_recheck_clears_unavailability_but_not_quota_block(self) -> None:
        provider = "gemini"
        model = "gemini-3.6-flash"
        runtime = self.state["runtime_slots"][f"{provider}:{model}"]
        runtime.update(
            {
                "status": "temporarily_unavailable",
                "retry_not_before": "2026-08-12T13:00:00Z",
                "authorized_recheck_task_id": "task-a",
            }
        )
        model_group = self.state["quota_groups"][f"{provider}:{model}"]
        model_group.update({"status": "deferred_quota", "retry_not_before": "2026-08-12T16:00:00Z"})
        quota_state.complete_slot_recheck(
            self.state,
            provider=provider,
            model=model,
            task_id="task-a",
            endpoint_available=True,
            now=NOW,
        )
        self.assertEqual(runtime["status"], "eligible")
        self.assertFalse(self.eligible(self.state, provider, model, now=NOW))

    def test_failed_recheck_extends_only_that_slot_cooldown(self) -> None:
        provider = "gemini"
        model = "gemini-3.6-flash"
        runtime = self.state["runtime_slots"][f"{provider}:{model}"]
        runtime.update(
            {
                "status": "temporarily_unavailable",
                "retry_not_before": "2026-08-12T13:00:00Z",
                "authorized_recheck_task_id": "task-a",
            }
        )
        quota_state.complete_slot_recheck(
            self.state,
            provider=provider,
            model=model,
            task_id="task-a",
            endpoint_available=False,
            now=NOW,
        )
        self.assertEqual(runtime["retry_not_before"], "2026-08-12T15:00:00Z")
        self.assertTrue(self.eligible(self.state, "groq", "openai/gpt-oss-20b"))

    def test_later_success_clears_transient_failure_from_same_managed_call(self) -> None:
        provider = "groq"
        model = "openai/gpt-oss-20b"
        failure = self.failure(provider, model, "503 temporarily unavailable")
        events = [
            self.event(
                event_id="attempt-1",
                provider=provider,
                model=model,
                observed_at="2026-08-12T14:00:00Z",
                outcome="failure",
                failure=failure,
            ),
            self.event(
                event_id="attempt-2",
                provider=provider,
                model=model,
                observed_at="2026-08-12T14:00:01Z",
            ),
        ]
        updated, _ = quota_state.aggregate_events(self.state, events, self.registry)
        self.assertEqual(updated["runtime_slots"][f"{provider}:{model}"]["status"], "eligible")

    def test_policy_block_requires_successful_free_policy_revalidation(self) -> None:
        provider = "openrouter"
        model = "openai/gpt-oss-20b:free"
        failure = self.failure(provider, model, "402 payment required; billing must be activated")
        updated, _ = quota_state.aggregate_events(
            self.state,
            [self.event(event_id="billing", provider=provider, model=model, outcome="failure", failure=failure)],
            self.registry,
        )
        self.assertEqual(failure.kind, "provider_policy_block")
        self.assertEqual(failure.scope, "provider")
        self.assertFalse(self.eligible(updated, provider, model))
        self.assertFalse(self.eligible(updated, provider, "google/gemma-4-31b-it:free"))
        self.assertTrue(self.eligible(updated, "gemini", "gemini-3.6-flash"))
        quota_state.record_audited_validation(
            updated,
            provider=provider,
            model=model,
            kind="free_policy",
            successful=False,
            timestamp="2026-08-12T15:00:00Z",
        )
        self.assertFalse(self.eligible(updated, provider, model))
        quota_state.record_audited_validation(
            updated,
            provider=provider,
            model=model,
            kind="free_policy",
            successful=True,
            timestamp="2026-08-12T16:00:00Z",
        )
        self.assertTrue(self.eligible(updated, provider, model))

    def test_model_price_policy_failure_blocks_only_the_exact_route(self) -> None:
        provider = "openrouter"
        model = "openai/gpt-oss-20b:free"
        failure = self.failure(
            provider,
            model,
            "provider_error_kind=provider_policy_block: completion pricing is not explicitly zero",
        )
        updated, _ = quota_state.aggregate_events(
            self.state,
            [self.event(event_id="route-price", provider=provider, model=model, outcome="failure", failure=failure)],
            self.registry,
        )
        self.assertEqual(failure.scope, "slot")
        self.assertFalse(self.eligible(updated, provider, model))
        self.assertTrue(self.eligible(updated, provider, "google/gemma-4-31b-it:free"))

    def test_batch_pre_call_guard_withholds_a_policy_blocked_slot(self) -> None:
        provider = "openrouter"
        model = "openai/gpt-oss-20b:free"
        self.state["runtime_slots"][f"{provider}:{model}"].update(
            {
                "status": "blocked_provider_policy",
                "block_reason": "provider_policy_block",
                "block_scope": "provider",
                "validation_required": True,
            }
        )
        planned = batch_runner.PlannedRun(
            1,
            "docs/stereotypes/classes/abstract.md",
            "page-hygiene-checker",
            provider,
            model,
            Path(".tmp/output.md"),
            Path(".tmp/output.batch.log"),
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            state_path = temporary_root / "quota-state.json"
            event_directory = temporary_root / "events"
            quota_state.write_state(state_path, self.state, self.registry)
            eligible, reason = batch_runner.pre_call_eligibility(
                planned=planned,
                repo_root=REPO_ROOT,
                max_completion_tokens=None,
                quota_state_path=state_path,
                quota_event_directory=event_directory,
                resolver_work_pending=False,
            )
        self.assertFalse(eligible)
        self.assertEqual(reason, "blocked_provider_policy")

    def test_authentication_block_is_provider_scoped_and_requires_audited_success(self) -> None:
        provider = "groq"
        model = "openai/gpt-oss-20b"
        failure = self.failure(provider, model, "status 401 invalid API key")
        updated, _ = quota_state.aggregate_events(
            self.state,
            [self.event(event_id="auth", provider=provider, model=model, outcome="failure", failure=failure)],
            self.registry,
        )
        self.assertEqual(failure.kind, "execution_configuration_block")
        self.assertFalse(failure.retryable_immediately)
        self.assertFalse(self.eligible(updated, provider, "openai/gpt-oss-120b"))
        self.assertTrue(self.eligible(updated, "gemini", "gemini-3.6-flash"))
        quota_state.record_audited_validation(
            updated,
            provider=provider,
            model=None,
            kind="execution_configuration",
            successful=False,
            timestamp="2026-08-12T15:00:00Z",
        )
        self.assertFalse(self.eligible(updated, provider, model))
        quota_state.record_audited_validation(
            updated,
            provider=provider,
            model=None,
            kind="execution_configuration",
            successful=True,
            timestamp="2026-08-12T16:00:00Z",
        )
        self.assertTrue(self.eligible(updated, provider, model))

    def test_deterministic_unsupported_parameter_blocks_only_the_slot(self) -> None:
        provider = "gemini"
        model = "gemini-3.6-flash"
        failure = self.failure(provider, model, "status 400 unsupported parameter: thinking_level")
        updated, _ = quota_state.aggregate_events(
            self.state,
            [self.event(event_id="parameter", provider=provider, model=model, outcome="failure", failure=failure)],
            self.registry,
        )
        self.assertEqual(failure.scope, "slot")
        self.assertFalse(failure.retryable_immediately)
        self.assertFalse(self.eligible(updated, provider, model))
        self.assertTrue(self.eligible(updated, provider, "gemini-3.5-flash-lite"))

    def test_identity_preserving_validation_unblocks_exact_task(self) -> None:
        identity = {"provider": "groq", "model": "openai/gpt-oss-20b", "content_sha256": "same"}
        task_id = task_identity.task_id_for(identity)
        tasks = task_state.new_task_state(registry_sha256="a" * 64, timestamp=TIMESTAMP)
        record = task_state.new_task_record(
            task_id=task_id,
            identity=identity,
            timestamp=TIMESTAMP,
            source_commit_sha=None,
        )
        record["status"] = "blocked_execution_configuration"
        tasks["tasks"][task_id] = record
        changed = quota_state.unblock_tasks_after_audited_validation(
            tasks,
            provider="groq",
            model="openai/gpt-oss-20b",
            blocked_status="blocked_execution_configuration",
            timestamp="2026-08-12T16:00:00Z",
        )
        self.assertEqual(changed, 1)
        self.assertEqual(tasks["tasks"][task_id]["status"], "pending")

    def test_identity_changing_correction_obsoletes_old_blocked_task(self) -> None:
        old_identity = {
            "provider": "openrouter",
            "model": "openai/gpt-oss-20b:free",
            "request_config_sha256": "old",
        }
        new_identity = {**old_identity, "request_config_sha256": "new"}
        old_id = task_identity.task_id_for(old_identity)
        new_id = task_identity.task_id_for(new_identity)
        initial = task_state.new_task_state(registry_sha256="a" * 64, timestamp=TIMESTAMP)
        record = task_state.new_task_record(
            task_id=old_id,
            identity=old_identity,
            timestamp=TIMESTAMP,
            source_commit_sha=None,
        )
        record["status"] = "blocked_provider_policy"
        initial["tasks"][old_id] = record
        reconciled, _ = task_reconciler.reconcile_task_state(
            existing_state=initial,
            desired_identities={new_id: new_identity},
            registry_sha256="b" * 64,
            configured_specs={("openrouter", "openai/gpt-oss-20b:free")},
            timestamp="2026-08-13T00:00:00Z",
            source_commit_sha=None,
        )
        self.assertEqual(reconciled["tasks"][old_id]["status"], "obsolete")
        self.assertEqual(reconciled["tasks"][new_id]["status"], "pending")

    def test_task_transition_uses_final_attempt_event(self) -> None:
        identity = {"provider": "groq", "model": "openai/gpt-oss-20b", "content_sha256": "same"}
        task_id = task_identity.task_id_for(identity)
        tasks = task_state.new_task_state(registry_sha256="a" * 64, timestamp=TIMESTAMP)
        tasks["tasks"][task_id] = task_state.new_task_record(
            task_id=task_id,
            identity=identity,
            timestamp=TIMESTAMP,
            source_commit_sha=None,
        )
        failure = self.failure("groq", "openai/gpt-oss-20b", "503 unavailable")
        events = [
            self.event(
                event_id="task-attempt-1",
                provider="groq",
                model="openai/gpt-oss-20b",
                observed_at="2026-08-12T14:00:00Z",
                outcome="failure",
                failure=failure,
                task_id=task_id,
            ),
            self.event(
                event_id="task-attempt-2",
                provider="groq",
                model="openai/gpt-oss-20b",
                observed_at="2026-08-12T14:00:01Z",
                task_id=task_id,
            ),
        ]
        changed = quota_state.apply_failure_events_to_task_state(tasks, events, ignored_event_ids=set())
        self.assertEqual(changed, 0)
        self.assertEqual(tasks["tasks"][task_id]["status"], "pending")

    def test_resolver_and_signal_events_share_provider_counters(self) -> None:
        events = [
            self.event(
                event_id="resolver-primary",
                provider="gemini",
                model="gemini-3.5-flash",
                call_source="resolver-primary",
            ),
            self.event(
                event_id="signal-gemini",
                provider="gemini",
                model="gemini-3.5-flash",
            ),
            self.event(
                event_id="resolver-fallback",
                provider="groq",
                model="openai/gpt-oss-120b",
                call_source="resolver-fallback",
            ),
        ]
        updated, _ = quota_state.aggregate_events(self.state, events, self.registry)
        self.assertEqual(updated["quota_groups"]["gemini:gemini-3.5-flash"]["requests_used_day_local"], 2)
        self.assertEqual(updated["quota_groups"]["gemini-project"]["requests_used_day_local"], 2)
        self.assertEqual(updated["quota_groups"]["groq:openai/gpt-oss-120b"]["requests_used_day_local"], 1)

    def test_resolver_priority_withholds_only_two_shared_signal_slots(self) -> None:
        self.assertFalse(
            self.eligible(
                self.state,
                "gemini",
                "gemini-3.5-flash",
                resolver_work_pending=True,
            )
        )
        self.assertFalse(
            self.eligible(
                self.state,
                "groq",
                "openai/gpt-oss-120b",
                resolver_work_pending=True,
            )
        )
        self.assertTrue(
            self.eligible(
                self.state,
                "gemini",
                "gemini-3.5-flash-lite",
                resolver_work_pending=True,
            )
        )
        self.assertTrue(self.eligible(self.state, "gemini", "gemini-3.5-flash"))

    def test_resolver_call_obeys_shared_quota_guard_before_provider_call(self) -> None:
        exhausted = self.state["quota_groups"]["gemini-project"]
        exhausted["status"] = "deferred_quota"
        exhausted["retry_not_before"] = "2026-08-12T15:00:00Z"
        with (
            mock.patch.object(resolver, "load_registry", return_value=self.registry),
            mock.patch.object(resolver, "load_quota_state", return_value=self.state),
            mock.patch.object(resolver, "load_event_files", return_value=[]),
            mock.patch.object(resolver, "datetime") as mocked_datetime,
            mock.patch.object(resolver, "call_gemini_json") as provider_call,
        ):
            mocked_datetime.now.return_value = NOW
            with self.assertRaisesRegex(
                resolver.ResolverError,
                "Resolver provider call withheld by quota/runtime guard",
            ):
                resolver.call_provider(
                    "gemini",
                    "gemini-3.5-flash",
                    "prompt",
                    "input",
                    8000,
                    1,
                )
        provider_call.assert_not_called()

    def test_resolver_guard_preserves_unavailability_fallback_signal(self) -> None:
        runtime = self.state["runtime_slots"]["gemini:gemini-3.5-flash"]
        runtime["status"] = "temporarily_unavailable"
        runtime["retry_not_before"] = "2026-08-12T15:00:00Z"
        with (
            mock.patch.object(resolver, "load_registry", return_value=self.registry),
            mock.patch.object(resolver, "load_quota_state", return_value=self.state),
            mock.patch.object(resolver, "load_event_files", return_value=[]),
            mock.patch.object(resolver, "datetime") as mocked_datetime,
            mock.patch.object(resolver, "call_gemini_json") as provider_call,
        ):
            mocked_datetime.now.return_value = NOW
            with self.assertRaisesRegex(
                resolver.ResolverError,
                "provider_error_kind=provider_unavailable",
            ):
                resolver.call_provider(
                    "gemini",
                    "gemini-3.5-flash",
                    "prompt",
                    "input",
                    8000,
                    1,
                )
        provider_call.assert_not_called()

    def test_daily_counters_reset_only_on_next_configured_period(self) -> None:
        event = self.event(event_id="day-one", provider="gemini", model="gemini-3.6-flash")
        same_day, _ = quota_state.aggregate_events(self.state, [event], self.registry)
        self.assertEqual(same_day["quota_groups"]["gemini-project"]["requests_used_day_local"], 1)
        next_event = self.event(
            event_id="day-two",
            provider="gemini",
            model="gemini-3.6-flash",
            observed_at="2026-08-13T00:00:00Z",
        )
        next_day, _ = quota_state.aggregate_events(same_day, [next_event], self.registry)
        self.assertEqual(next_day["quota_groups"]["gemini-project"]["requests_used_day_local"], 1)
        self.assertEqual(next_day["counter_period"]["daily_period_start"], "2026-08-13")

    def test_provider_event_is_replayable_and_does_not_store_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            secret = "gsk_this_should_be_redacted_123456789"
            with mock.patch.dict(
                os.environ,
                {
                    "PHASE2_QUOTA_EVENT_DIR": directory,
                    "PHASE2_CALL_SOURCE": "resolver-primary",
                    "PHASE2_TASK_ID": "task-123",
                },
                clear=False,
            ):
                provider_runtime.record_provider_failure(
                    provider="groq",
                    model="openai/gpt-oss-120b",
                    exc=HeaderError(f"status 401 Authorization: {secret}"),
                    request_sent=True,
                    observed_at=NOW,
                )
            paths = list(Path(directory).glob("*.json"))
            self.assertEqual(len(paths), 1)
            payload = paths[0].read_text(encoding="utf-8")
            event = json.loads(payload)
            self.assertNotIn(secret, payload)
            self.assertEqual(event["call_source"], "resolver-primary")
            self.assertEqual(event["task_id"], "task-123")

    def test_provider_event_redacts_bearer_credential(self) -> None:
        credential = "opaque-sensitive-credential"
        diagnostic = provider_runtime.safe_diagnostic(HeaderError(f"Authorization: Bearer {credential}"))
        self.assertNotIn(credential, diagnostic)
        self.assertEqual(diagnostic, "Authorization: <redacted>")

    def test_provider_event_redacts_json_shaped_api_key(self) -> None:
        credential = "opaque-sensitive-credential"
        error = HeaderError("request failed")
        error.body = {"api_key": credential}
        diagnostic = provider_runtime.safe_diagnostic(error)
        self.assertNotIn(credential, diagnostic)
        self.assertIn("'api_key': <redacted>", diagnostic)

    def test_same_second_retry_events_replay_in_recorded_order(self) -> None:
        model = "gemini-3.5-flash"
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.dict(os.environ, {"PHASE2_QUOTA_EVENT_DIR": directory}, clear=False),
            mock.patch.object(provider_runtime.time, "time_ns", side_effect=[100, 101]),
            mock.patch.object(provider_runtime.uuid, "uuid4", side_effect=["z", "a"]),
        ):
            provider_runtime.record_provider_failure(
                provider="gemini",
                model=model,
                exc=HeaderError("503 Service Unavailable"),
                request_sent=True,
                observed_at=NOW,
            )
            provider_runtime.record_provider_event(
                provider="gemini",
                model=model,
                outcome="success",
                request_sent=True,
                observed_at=NOW,
            )
            events = quota_state.load_event_files(Path(directory))
        updated, _ = quota_state.aggregate_events(self.state, events, self.registry)
        self.assertEqual(updated["runtime_slots"][f"gemini:{model}"]["status"], "eligible")
        self.assertEqual(updated["quota_groups"]["gemini-project"]["requests_used_day_local"], 2)


if __name__ == "__main__":
    unittest.main()
