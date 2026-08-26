"""Tests for compact Phase 2 signal prompts and stable prompt identity."""

from __future__ import annotations

import importlib
import math
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPT_DIR = REPO_ROOT / "scripts" / "phase-2"
if str(PHASE2_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPT_DIR))

run_check_agent = importlib.import_module("run_check_agent")
provider_model_registry = importlib.import_module("provider_model_registry")
task_identity = importlib.import_module("task_identity")

PAGE = "# Kind\n\nSentence one.\n\nSentence two.\n\nSentence three.\n"
REVIEW_DATE = "2026-08-17"
PAGE_PATH = "docs/stereotypes/classes/kind.md"
COMMIT_SHA = "a" * 40

NO_SIGNAL_SUMMARIES = {
    "page-hygiene-checker": "No page-hygiene signals were identified within the configured scope.",
    "language-style-checker": "No language-style signals were identified within the configured scope.",
}
SCOPES = {
    "page-hygiene-checker": (
        "Page-hygiene check only. This run reviewed visible reference hygiene, Markdown hygiene, encoding "
        "hygiene, and Generation and Review Log hygiene in the provided page only."
    ),
    "language-style-checker": (
        "Language-style check only. This run reviewed grammar, spelling, clarity, professional technical "
        "style, and project self-reference in the provided page only."
    ),
}


def no_signal_report(agent: str) -> str:
    prompt_id = run_check_agent.AGENT_CONTRACTS[agent].prompt_id
    return f"""## Check signal report: {agent} / groq / model — {REVIEW_DATE}

### Run metadata

| Field | Value |
|---|---|
| Agent | {agent} |
| Provider | groq |
| Model | model |
| Prompt | {prompt_id} |
| Review date | {REVIEW_DATE} |
| Reviewed page | {PAGE_PATH} |
| Commit SHA | {COMMIT_SHA} |
| Signal count | 0 |

### Summary judgment

{NO_SIGNAL_SUMMARIES[agent]}

### Scope

{SCOPES[agent]}

### Signals

None identified within the configured check-agent scope.
"""


def three_signal_report() -> str:
    agent = "language-style-checker"
    prompt_id = run_check_agent.AGENT_CONTRACTS[agent].prompt_id
    blocks = []
    for index, fragment in enumerate(("Sentence one.", "Sentence two.", "Sentence three."), start=1):
        blocks.append(
            f"""#### S-{index:03d} — Clear local wording issue

- Category: `clarity`
- Severity: `medium`
- Confidence: `high`
- Location: Section: "Kind"; Fragment: "{fragment}"
- Observation: The sentence has a localized clarity problem.
- Rationale: The wording is difficult to parse. A local revision would improve readability without changing meaning.
- Recommendation: Revise only the identified sentence for clarity while preserving its meaning.
"""
        )
    return f"""## Check signal report: {agent} / groq / model — {REVIEW_DATE}

### Run metadata

| Field | Value |
|---|---|
| Agent | {agent} |
| Provider | groq |
| Model | model |
| Prompt | {prompt_id} |
| Review date | {REVIEW_DATE} |
| Reviewed page | {PAGE_PATH} |
| Commit SHA | {COMMIT_SHA} |
| Signal count | 3 |

### Summary judgment

Language-style signals were identified that may affect standalone professional documentation quality.

### Scope

{SCOPES[agent]}

### Signals

{"".join(blocks)}"""


class PromptCompactionTests(unittest.TestCase):
    def effective_prompt(self, agent: str) -> str:
        return run_check_agent.load_effective_prompt(
            repo_root=REPO_ROOT,
            contract=run_check_agent.AGENT_CONTRACTS[agent],
        )

    def test_effective_prompts_retain_shared_and_agent_specific_requirements(self) -> None:
        shared_requirements = (
            "Return exactly one Markdown GitHub issue comment",
            "Use only the supplied run metadata and agent-scoped canonical page Markdown",
            "Report at most three highest-priority signals",
            "current_text` and `proposed_text` are optional",
            "None identified within the configured check-agent scope.",
            "Do not expose analysis or provider reasoning",
        )
        agent_requirements = {
            "page-hygiene-checker": (
                "visible reference hygiene",
                "Markdown hygiene",
                "encoding hygiene",
                "Generation and Review Log hygiene",
                "reference_hygiene",
                "| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |",
            ),
            "language-style-checker": (
                "grammar",
                "spelling",
                "clarity",
                "professional technical style",
                "project_self_reference",
            ),
        }
        for agent in run_check_agent.AGENT_CONTRACTS:
            with self.subTest(agent=agent):
                prompt = self.effective_prompt(agent)
                for requirement in (*shared_requirements, *agent_requirements[agent]):
                    self.assertIn(requirement, prompt)

    def test_shared_extraction_reduces_static_prompt_content(self) -> None:
        old_versions = {
            "page-hygiene-checker": "prompts/phase-2/page-hygiene-checker-v1.0.3.md",
            "language-style-checker": "prompts/phase-2/language-style-checker-v1.0.3.md",
        }
        for agent, old_path in old_versions.items():
            with self.subTest(agent=agent):
                old_prompt = (REPO_ROOT / old_path).read_text(encoding="utf-8")
                self.assertLess(len(self.effective_prompt(agent)), len(old_prompt))

    def test_prompt_ids_and_hashes_are_stable(self) -> None:
        expected = {
            "page-hygiene-checker": (
                "page-hygiene-checker-v1.1.1",
                "a3f5e548514f8018b4ab44dc3d07945378b6522b98a28d6f422f12518e829d08",
            ),
            "language-style-checker": (
                "language-style-checker-v1.1.0",
                "857e94c7a3d3fd13a90f42558796f9b6657d5f1a433e5d707b9336b4e02b349f",
            ),
        }
        for agent, (prompt_id, prompt_hash) in expected.items():
            with self.subTest(agent=agent):
                contract = run_check_agent.AGENT_CONTRACTS[agent]
                self.assertEqual(contract.prompt_id, prompt_id)
                effective = task_identity.build_effective_prompt_content(
                    checker_prompt=self.effective_prompt(agent),
                    agent=agent,
                    prompt_id=prompt_id,
                    input_scope_note=task_identity.scope_page_content_for_agent(agent=agent, page_content=PAGE)[1],
                )
                self.assertEqual(task_identity.sha256_text(effective), prompt_hash)

    def test_mutable_run_metadata_does_not_change_stable_prompt_hash(self) -> None:
        prompt = self.effective_prompt("page-hygiene-checker")
        stable = task_identity.build_effective_prompt_content(
            checker_prompt=prompt,
            agent="page-hygiene-checker",
            prompt_id="page-hygiene-checker-v1.1.1",
            input_scope_note="full canonical stereotype page",
        )
        first = task_identity.build_review_input(
            checker_prompt=prompt,
            agent="page-hygiene-checker",
            provider="groq",
            model="first",
            prompt_id="page-hygiene-checker-v1.1.1",
            review_date="2026-08-17",
            page_path="first.md",
            commit_sha="a" * 40,
            max_completion_tokens=3000,
            page_content="first",
            input_scope_note="full canonical stereotype page",
        )
        second = task_identity.build_review_input(
            checker_prompt=prompt,
            agent="page-hygiene-checker",
            provider="gemini",
            model="second",
            prompt_id="page-hygiene-checker-v1.1.1",
            review_date="2026-08-18",
            page_path="second.md",
            commit_sha="b" * 40,
            max_completion_tokens=2500,
            page_content="second",
            input_scope_note="full canonical stereotype page",
        )
        self.assertNotEqual(first, second)
        for mutable_value in ("groq", "gemini", "first.md", "second.md", "a" * 40, "b" * 40):
            self.assertNotIn(mutable_value, stable)
        registry = provider_model_registry.load_registry(REPO_ROOT / "config/phase-2/provider-models.json")
        identities = [
            task_identity.build_task_identity(
                page=PAGE_PATH,
                agent="page-hygiene-checker",
                provider=slot.provider,
                model=slot.model,
                page_content=PAGE,
                prompt_id="page-hygiene-checker-v1.1.1",
                prompt_content=prompt,
                slot=slot,
            )
            for slot in (registry.configured_slots[0], registry.configured_slots[6])
        ]
        self.assertEqual(identities[0]["prompt_sha256"], identities[1]["prompt_sha256"])

    def test_prompt_fixtures_pass_existing_validator(self) -> None:
        for agent, contract in run_check_agent.AGENT_CONTRACTS.items():
            with self.subTest(agent=agent):
                errors = run_check_agent.validate_issue_comment(
                    text=no_signal_report(agent),
                    contract=contract,
                    provider="groq",
                    model="model",
                    prompt_id=contract.prompt_id,
                    review_date=REVIEW_DATE,
                    page_path=PAGE_PATH,
                    commit_sha=COMMIT_SHA,
                    page_content=PAGE,
                )
                self.assertEqual(errors, [])

    def test_maximum_three_signal_fixture_fits_output_cap(self) -> None:
        report = three_signal_report()
        contract = run_check_agent.AGENT_CONTRACTS["language-style-checker"]
        errors = run_check_agent.validate_issue_comment(
            text=report,
            contract=contract,
            provider="groq",
            model="model",
            prompt_id=contract.prompt_id,
            review_date=REVIEW_DATE,
            page_path=PAGE_PATH,
            commit_sha=COMMIT_SHA,
            page_content=PAGE,
        )
        conservative_token_estimate = math.ceil(len(report.encode("utf-8")) / 4)
        self.assertEqual(errors, [])
        self.assertLess(conservative_token_estimate, 3000)


if __name__ == "__main__":
    unittest.main()
