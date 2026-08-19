"""Tests for Phase 2 content-addressed task identity and persistent state."""

from __future__ import annotations

import copy
import importlib
import sys
import unittest
from dataclasses import replace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPT_DIR = REPO_ROOT / "scripts" / "phase-2"
if str(PHASE2_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPT_DIR))

issue_manager = importlib.import_module("issue_manager")
registry_module = importlib.import_module("provider_model_registry")
task_identity = importlib.import_module("task_identity")
task_reconciler = importlib.import_module("task_reconciler")
task_state = importlib.import_module("task_state")

REGISTRY_PATH = REPO_ROOT / "config" / "phase-2" / "provider-models.json"
TASK_STATE_PATH = REPO_ROOT / "data" / "phase-2" / "task-state.json"
TIMESTAMP = "2026-08-12T00:00:00Z"


class TaskIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = registry_module.load_registry(REGISTRY_PATH)
        cls.slot = cls.registry.configured_slots[0]

    def identity(
        self,
        *,
        page_content: str = "# Kind\n\nReader-facing text.\n",
        prompt_content: str = "Review the page.\n",
        agent: str = "page-hygiene-checker",
        slot=None,
    ) -> dict[str, str]:
        selected_slot = slot or self.slot
        return task_identity.build_task_identity(
            page="docs/stereotypes/classes/kind.md",
            agent=agent,
            provider=selected_slot.provider,
            model=selected_slot.model,
            page_content=page_content,
            prompt_id=f"{agent}-v1.0.3",
            prompt_content=prompt_content,
            slot=selected_slot,
        )

    def test_identical_relevant_inputs_produce_identical_ids(self) -> None:
        self.assertEqual(
            task_identity.task_id_for(self.identity()),
            task_identity.task_id_for(self.identity()),
        )

    def test_line_ending_normalization_is_the_only_text_normalization(self) -> None:
        lf_identity = self.identity(page_content="# Kind\n\nExact  spacing.\n")
        crlf_identity = self.identity(page_content="# Kind\r\n\r\nExact  spacing.\r\n")
        wording_change = self.identity(page_content="# Kind\n\nExact spacing.\n")
        self.assertEqual(lf_identity["content_sha256"], crlf_identity["content_sha256"])
        self.assertNotEqual(lf_identity["content_sha256"], wording_change["content_sha256"])

    def test_commit_statistics_and_unrelated_page_metadata_do_not_change_id(self) -> None:
        identity = self.identity()
        first = task_state.new_task_record(
            task_id=task_identity.task_id_for(identity),
            identity=identity,
            timestamp=TIMESTAMP,
            source_commit_sha="a" * 40,
        )
        second = task_state.new_task_record(
            task_id=task_identity.task_id_for(identity),
            identity=identity,
            timestamp=TIMESTAMP,
            source_commit_sha="b" * 40,
        )
        self.assertEqual(first["task_id"], second["task_id"])
        self.assertNotEqual(first["source_metadata"], second["source_metadata"])

    def test_relevant_page_change_creates_new_task(self) -> None:
        before = task_identity.task_id_for(self.identity(page_content="# Kind\n\nBefore.\n"))
        after = task_identity.task_id_for(self.identity(page_content="# Kind\n\nAfter.\n"))
        self.assertNotEqual(before, after)

    def test_excluded_language_style_section_does_not_change_content_hash(self) -> None:
        first = self.identity(
            agent="language-style-checker",
            page_content="# Kind\n\nReader-facing.\n\n## References\n\nFirst citation.\n",
        )
        second = self.identity(
            agent="language-style-checker",
            page_content="# Kind\n\nReader-facing.\n\n## References\n\nDifferent citation.\n",
        )
        self.assertEqual(first["content_sha256"], second["content_sha256"])

    def test_provider_and_model_route_are_identity_fields(self) -> None:
        groq_slot = next(slot for slot in self.registry.configured_slots if slot.provider == "groq")
        self.assertNotEqual(
            task_identity.task_id_for(self.identity()),
            task_identity.task_id_for(self.identity(slot=groq_slot)),
        )

    def test_same_model_through_different_providers_creates_different_task(self) -> None:
        alternate_route = replace(self.slot, provider="groq")
        first = self.identity(slot=self.slot)
        second = self.identity(slot=alternate_route)
        self.assertEqual(first["model"], second["model"])
        self.assertNotEqual(first["provider"], second["provider"])
        self.assertNotEqual(task_identity.task_id_for(first), task_identity.task_id_for(second))

    def test_prompt_content_change_creates_new_task(self) -> None:
        before = task_identity.task_id_for(self.identity(prompt_content="First prompt.\n"))
        after = task_identity.task_id_for(self.identity(prompt_content="Changed prompt.\n"))
        self.assertNotEqual(before, after)

    def test_prompt_hash_covers_the_stable_effective_prompt(self) -> None:
        prompt_content = "Review the page.\n"
        identity = self.identity(prompt_content=prompt_content)
        effective_prompt = task_identity.build_effective_prompt_content(
            checker_prompt=prompt_content,
            agent="page-hygiene-checker",
            prompt_id="page-hygiene-checker-v1.0.3",
            input_scope_note="full canonical stereotype page",
        )
        self.assertEqual(identity["prompt_sha256"], task_identity.sha256_text(effective_prompt))
        self.assertNotEqual(identity["prompt_sha256"], task_identity.sha256_text(prompt_content))

    def test_request_reasoning_change_creates_new_task(self) -> None:
        changed_config = dict(self.slot.request_config)
        changed_config["reasoning"] = "different-supported-mode"
        changed_slot = replace(self.slot, request_config=changed_config)
        before = task_identity.task_id_for(self.identity())
        after = task_identity.task_id_for(self.identity(slot=changed_slot))
        self.assertNotEqual(before, after)


class TaskReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = registry_module.load_registry(REGISTRY_PATH)

    def test_repository_reconciliation_universe_has_exactly_1950_tasks(self) -> None:
        desired = task_reconciler.build_desired_task_identities(repo_root=REPO_ROOT, registry=self.registry)
        self.assertEqual(len(desired), 1950)
        self.assertEqual(len(set(desired)), 1950)

    def test_checked_in_state_has_1950_desired_tasks_and_retired_history(self) -> None:
        desired = task_reconciler.build_desired_task_identities(repo_root=REPO_ROOT, registry=self.registry)
        state = task_state.load_task_state(TASK_STATE_PATH)
        registry_sha = task_identity.sha256_text(REGISTRY_PATH.read_text(encoding="utf-8"))
        task_reconciler.validate_desired_state(state, desired, registry_sha)
        self.assertEqual(len(state["tasks"]), 4836)
        self.assertEqual(len(desired), 1950)
        self.assertEqual(
            sum(record["status"] == "retired" for record in state["tasks"].values()),
            540,
        )

    def test_superseded_task_becomes_obsolete(self) -> None:
        old_identity = {"provider": "groq", "model": "model", "content_sha256": "old"}
        new_identity = {"provider": "groq", "model": "model", "content_sha256": "new"}
        old_id = task_identity.task_id_for(old_identity)
        new_id = task_identity.task_id_for(new_identity)
        initial = task_state.new_task_state(registry_sha256="a" * 64, timestamp=TIMESTAMP)
        initial["tasks"][old_id] = task_state.new_task_record(
            task_id=old_id,
            identity=old_identity,
            timestamp=TIMESTAMP,
            source_commit_sha=None,
        )
        reconciled, counts = task_reconciler.reconcile_task_state(
            existing_state=initial,
            desired_identities={new_id: new_identity},
            registry_sha256="b" * 64,
            configured_specs={("groq", "model")},
            timestamp="2026-08-13T00:00:00Z",
            source_commit_sha=None,
        )
        self.assertEqual(reconciled["tasks"][old_id]["status"], "obsolete")
        self.assertEqual(reconciled["tasks"][new_id]["status"], "pending")
        self.assertEqual(counts["obsolete"], 1)
        self.assertEqual(counts["added"], 1)

    def test_completed_desired_task_remains_completed(self) -> None:
        identity = {"provider": "groq", "model": "model", "content_sha256": "same"}
        task_id = task_identity.task_id_for(identity)
        initial = task_state.new_task_state(registry_sha256="a" * 64, timestamp=TIMESTAMP)
        record = task_state.new_task_record(
            task_id=task_id,
            identity=identity,
            timestamp=TIMESTAMP,
            source_commit_sha=None,
        )
        record["status"] = "completed"
        initial["tasks"][task_id] = record
        reconciled, counts = task_reconciler.reconcile_task_state(
            existing_state=initial,
            desired_identities={task_id: copy.deepcopy(identity)},
            registry_sha256="b" * 64,
            configured_specs={("groq", "model")},
            timestamp="2026-08-13T00:00:00Z",
            source_commit_sha=None,
        )
        self.assertEqual(reconciled["tasks"][task_id]["status"], "completed")
        self.assertEqual(counts["preserved"], 1)
        self.assertEqual(counts["added"], 0)


class IssueCommentIdentityTests(unittest.TestCase):
    def metadata(self, commit_sha: str) -> issue_manager.ReviewCommentMetadata:
        return issue_manager.ReviewCommentMetadata(
            reviewed_page="docs/stereotypes/classes/kind.md",
            signal_count=1,
            agent="language-style-checker",
            provider="groq",
            model="openai/gpt-oss-20b",
            prompt="language-style-checker-v1.0.3",
            commit_sha=commit_sha,
        )

    def test_content_addressed_comment_identity_ignores_commit_sha(self) -> None:
        task_id = "c" * 64
        first = issue_manager.build_comment_identity(self.metadata("a" * 40), task_id)
        second = issue_manager.build_comment_identity(self.metadata("b" * 40), task_id)
        self.assertEqual(first, second)
        self.assertNotIn("commit", first)
        self.assertEqual(first["task_id"], task_id)

    def test_content_addressed_agents_require_task_id(self) -> None:
        with self.assertRaisesRegex(issue_manager.IssueManagerError, "--task-id is required"):
            issue_manager.build_comment_identity(self.metadata("a" * 40))


if __name__ == "__main__":
    unittest.main()
