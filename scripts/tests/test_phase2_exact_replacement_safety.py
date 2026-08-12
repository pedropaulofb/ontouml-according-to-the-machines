"""Regression tests for deterministic Phase 2 exact-replacement safety."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


check_agent = load_module(
    "phase_2_run_check_agent_exact_replacement_tests",
    REPO_ROOT / "scripts" / "phase-2" / "run_check_agent.py",
)
resolver = load_module(
    "phase_2_resolve_signal_issue_exact_replacement_tests",
    REPO_ROOT / "scripts" / "phase-2" / "resolve_signal_issue.py",
)


class CheckAgentExactReplacementTests(unittest.TestCase):
    def report(
        self,
        *,
        current_text: str | None = None,
        proposed_text: str | None = None,
        location_fragment: str = "Sect. 2.1.",
        location_section: str = "Description",
    ) -> str:
        optional = ""
        if current_text is not None:
            optional += f'\n- current_text: "{current_text}"'
        if proposed_text is not None:
            optional += f'\n- proposed_text: "{proposed_text}"'
        return f"""## Check signal report: language-style-checker / gemini / test-model — 2026-07-11

### Run metadata

| Field | Value |
|---|---|
| Agent | language-style-checker |
| Provider | gemini |
| Model | test-model |
| Prompt | language-style-checker-v1.0.3 |
| Review date | 2026-07-11 |
| Reviewed page | docs/stereotypes/classes/example.md |
| Commit SHA | abc123 |
| Signal count | 1 |

### Summary judgment

Minor language-style signals were identified; they mainly affect readability or professional style.

### Scope

Language-style check only. This run reviewed grammar, spelling, clarity, professional technical style, and project self-reference in the provided page only.

### Signals

#### S-001 — Abbreviated section label

- Category: `professional_style`
- Severity: `low`
- Confidence: `high`
- Location: Section: "{location_section}"; Fragment: "{location_fragment}"
- Observation: The abbreviated section label is inconsistent with the surrounding style.
- Rationale: The issue is visible and meaning-preserving to correct.
- Recommendation: Use the unabbreviated section label.{optional}
"""

    def validate(self, text: str, page_content: str) -> list[str]:
        return check_agent.validate_issue_comment(
            text=text,
            contract=check_agent.AGENT_CONTRACTS["language-style-checker"],
            provider="gemini",
            model="test-model",
            prompt_id="language-style-checker-v1.0.3",
            review_date="2026-07-11",
            page_path="docs/stereotypes/classes/example.md",
            commit_sha="abc123",
            page_content=page_content,
        )

    def run_main_with_report(self, *, page: str, report: str) -> tuple[int, str | None, str | None]:
        """Run the real check-agent entry point and capture normal/invalid output text."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prompt_path = root / "prompt.md"
            page_path = root / "docs/stereotypes/classes/example.md"
            output_path = root / "output.md"
            invalid_path = output_path.with_suffix(".invalid.md")
            prompt_path.write_text("Prompt", encoding="utf-8")
            page_path.parent.mkdir(parents=True)
            page_path.write_text(page, encoding="utf-8")
            args = argparse.Namespace(
                agent="language-style-checker",
                page="docs/stereotypes/classes/example.md",
                provider="gemini",
                model="test-model",
                output="output.md",
                prompt="prompt.md",
                prompt_id="language-style-checker-v1.0.3",
                commit_sha="abc123",
                review_date="2026-07-11",
                max_completion_tokens=3000,
            )
            with (
                mock.patch.object(check_agent, "parse_args", return_value=args),
                mock.patch.object(check_agent, "get_repo_root", return_value=root),
                mock.patch.object(
                    check_agent,
                    "require_executable_slot",
                    return_value=mock.Mock(
                        agents=("language-style-checker",),
                        spec="gemini:test-model",
                        max_completion_tokens=3000,
                    ),
                ),
                mock.patch.object(check_agent, "load_provider", return_value=mock.Mock(return_value=report)),
            ):
                result = check_agent.main()
            output_text = output_path.read_text(encoding="utf-8") if output_path.exists() else None
            invalid_text = invalid_path.read_text(encoding="utf-8") if invalid_path.exists() else None
        return result, output_text, invalid_text

    def test_run_input_reinforces_minimal_unambiguous_targeting_without_replacing_versioned_prompt(
        self,
    ) -> None:
        review_input = check_agent.build_review_input(
            checker_prompt="Existing versioned prompt",
            agent="language-style-checker",
            provider="gemini",
            model="test-model",
            prompt_id="language-style-checker-v1.0.3",
            review_date="2026-07-11",
            page_path="docs/stereotypes/classes/example.md",
            commit_sha="abc123",
            max_completion_tokens=3000,
            page_content="## Description\n\nText.\n",
            input_scope_note="reader-facing page content only",
        )

        self.assertIn("Existing versioned prompt", review_input)
        self.assertIn(
            "A signal may describe one problem that occurs once or multiple times.",
            review_input,
        )
        self.assertIn("smallest reasonably sufficient contiguous context", review_input)
        self.assertIn("omit both optional replacement fields", review_input)

    def test_one_uniquely_identifiable_occurrence_is_preserved(self) -> None:
        page = "## Description\n\nSee Sect. 2.1. for details.\n"
        report = self.report(current_text="Sect. 2.1.", proposed_text="Section 2.1.")

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)

        self.assertEqual(messages, [])
        self.assertIn('- current_text: "Sect. 2.1."', normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_unique_target_outside_declared_location_is_omitted_and_signal_is_preserved(
        self,
    ) -> None:
        page = "## Description\n\nThe visible issue is Sect. 2.1. The unrelated target is Elsewhere.\n"
        report = self.report(
            current_text="Elsewhere.",
            proposed_text="Somewhere else.",
            location_fragment="Sect. 2.1.",
        )

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)

        self.assertEqual(len(messages), 1)
        self.assertIn("did not correspond", messages[0])
        self.assertIn("#### S-001 — Abbreviated section label", normalized)
        self.assertNotIn("current_text", normalized)
        self.assertNotIn("proposed_text", normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_direct_validation_rejects_unique_target_outside_declared_location(
        self,
    ) -> None:
        page = "## Description\n\nThe visible issue is Sect. 2.1. The unrelated target is Elsewhere.\n"
        report = self.report(
            current_text="Elsewhere.",
            proposed_text="Somewhere else.",
            location_fragment="Sect. 2.1.",
        )

        errors = self.validate(report, page)

        self.assertTrue(any("must correspond" in error for error in errors))

    def test_unique_target_under_declared_section_is_preserved_when_fragment_repeats_elsewhere(self) -> None:
        page = "## Section A\n\nUnique prefix shared fragment target.\n\n## Section B\n\nshared fragment only.\n"
        report = self.report(
            current_text="Unique prefix shared fragment target.",
            proposed_text="Improved target.",
            location_fragment="shared fragment",
            location_section="Section A",
        )

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)

        self.assertEqual(messages, [])
        self.assertIn('- current_text: "Unique prefix shared fragment target."', normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_unique_target_in_wrong_declared_section_is_omitted_and_signal_is_preserved(self) -> None:
        page = "## Section A\n\nUnique prefix shared fragment target.\n\n## Section B\n\nshared fragment only.\n"
        report = self.report(
            current_text="Unique prefix shared fragment target.",
            proposed_text="Improved target.",
            location_fragment="shared fragment",
            location_section="Section B",
        )

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)

        self.assertEqual(len(messages), 1)
        self.assertIn("declared Location fragment and section", messages[0])
        self.assertNotIn("current_text", normalized)
        self.assertNotIn("proposed_text", normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_wrong_section_target_is_not_sanitized_when_declared_location_is_not_grounded(self) -> None:
        page = "## Section A\n\nUnique prefix shared fragment target.\n"
        report = self.report(
            current_text="Unique prefix shared fragment target.",
            proposed_text="Improved target.",
            location_fragment="shared fragment",
            location_section="Section B",
        )

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)
        errors = self.validate(normalized, page)

        self.assertEqual(messages, [])
        self.assertIn('- current_text: "Unique prefix shared fragment target."', normalized)
        self.assertTrue(any("declared Location fragment and section" in error for error in errors))

    def test_direct_validation_rejects_unique_target_in_wrong_declared_section(self) -> None:
        page = "## Section A\n\nUnique prefix shared fragment target.\n\n## Section B\n\nshared fragment only.\n"
        report = self.report(
            current_text="Unique prefix shared fragment target.",
            proposed_text="Improved target.",
            location_fragment="shared fragment",
            location_section="Section B",
        )

        errors = self.validate(report, page)

        self.assertTrue(any("declared Location fragment and section" in error for error in errors))

    def test_ungrounded_location_fragment_containing_unique_target_is_not_sanitized(self) -> None:
        page = "## Description\n\nActual target.\n"
        report = self.report(
            current_text="Actual target.",
            proposed_text="Improved target.",
            location_fragment="Actual target. fabricated suffix",
        )

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)
        errors = self.validate(normalized, page)

        self.assertEqual(messages, [])
        self.assertIn('- current_text: "Actual target."', normalized)
        self.assertTrue(any("declared Location fragment and section" in error for error in errors))

    def test_direct_validation_rejects_ungrounded_location_fragment_containing_unique_target(self) -> None:
        page = "## Description\n\nActual target.\n"
        report = self.report(
            current_text="Actual target.",
            proposed_text="Improved target.",
            location_fragment="Actual target. fabricated suffix",
        )

        errors = self.validate(report, page)

        self.assertTrue(any("declared Location fragment and section" in error for error in errors))

    def test_ambiguous_exact_target_is_omitted_and_signal_is_preserved(self) -> None:
        page = "## Description\n\nSee Sect. 2.1. first. See Sect. 2.1. again.\n"
        report = self.report(current_text="Sect. 2.1.", proposed_text="Section 2.1.")

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)

        self.assertEqual(len(messages), 1)
        self.assertIn("matched 2 location(s)", messages[0])
        self.assertIn("#### S-001 — Abbreviated section label", normalized)
        self.assertNotIn("current_text", normalized)
        self.assertNotIn("proposed_text", normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_zero_match_exact_target_is_omitted_and_signal_is_preserved(self) -> None:
        page = "## Description\n\nThe visible issue is Sect. 2.1., but the proposed target is stale.\n"
        report = self.report(current_text="Old wording.", proposed_text="New wording.")

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)

        self.assertEqual(len(messages), 1)
        self.assertIn("matched 0 location(s)", messages[0])
        self.assertIn("#### S-001 — Abbreviated section label", normalized)
        self.assertNotIn("current_text", normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_zero_match_target_is_not_sanitized_when_location_is_not_page_grounded(
        self,
    ) -> None:
        page = "## Description\n\nThe current page contains unrelated wording.\n"
        report = self.report(
            current_text="Old wording.",
            proposed_text="New wording.",
            location_fragment="Missing location fragment.",
        )

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)
        errors = self.validate(normalized, page)

        self.assertEqual(messages, [])
        self.assertIn('- current_text: "Old wording."', normalized)
        self.assertTrue(any("found 0 matches" in error for error in errors))

    def test_overlapping_occurrences_are_treated_as_ambiguous(self) -> None:
        page = "## Description\n\naaaa\n"
        report = self.report(current_text="aaa", proposed_text="bbb", location_fragment="aaa")

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)

        self.assertEqual(len(messages), 1)
        self.assertIn("matched 2 location(s)", messages[0])
        self.assertNotIn("current_text", normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_grounded_placeholder_pair_is_removed_and_signal_is_preserved(self) -> None:
        page = "## Description\n\nSee Sect. 2.1. for details.\n"
        report = self.report(current_text="None", proposed_text="N/A")
        report = report.replace('- current_text: "None"', "- current_text: None")
        report = report.replace('- proposed_text: "N/A"', "- proposed_text: N/A")

        normalized = check_agent.normalize_issue_comment(
            report,
            check_agent.AGENT_CONTRACTS["language-style-checker"],
        )
        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(normalized, page)

        self.assertEqual(len(messages), 1)
        self.assertIn("recognized placeholder value", messages[0])
        self.assertNotIn("current_text", normalized)
        self.assertNotIn("proposed_text", normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_grounded_quoted_placeholder_pair_is_removed_and_signal_is_preserved(self) -> None:
        page = "## Description\n\nSee Sect. 2.1. for details.\n"
        report = self.report(current_text="None", proposed_text="Not applicable")

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)

        self.assertEqual(len(messages), 1)
        self.assertIn("recognized placeholder value", messages[0])
        self.assertNotIn("current_text", normalized)
        self.assertNotIn("proposed_text", normalized)
        self.assertEqual(self.validate(normalized, page), [])

    def test_ungrounded_placeholder_pair_is_left_visible_for_strict_rejection(self) -> None:
        page = "## Description\n\nCurrent wording.\n"
        report = self.report(current_text="None", proposed_text="N/A")
        report = report.replace('- current_text: "None"', "- current_text: None")
        report = report.replace('- proposed_text: "N/A"', "- proposed_text: N/A")

        normalized = check_agent.normalize_issue_comment(
            report,
            check_agent.AGENT_CONTRACTS["language-style-checker"],
        )
        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(normalized, page)
        errors = self.validate(normalized, page)

        self.assertEqual(messages, [])
        self.assertIn("- current_text: None", normalized)
        self.assertIn("- proposed_text: N/A", normalized)
        self.assertTrue(any("must be wrapped in double quotation marks" in error for error in errors))

    def test_unchanged_pair_is_not_sanitized_into_a_valid_signal(self) -> None:
        page = "## Description\n\nRepeat. Repeat.\n"
        report = self.report(current_text="Repeat.", proposed_text="Repeat.")

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, page)
        errors = self.validate(normalized, page)

        self.assertEqual(messages, [])
        self.assertIn('- current_text: "Repeat."', normalized)
        self.assertTrue(any("must differ" in error for error in errors))
        self.assertTrue(any("found 2 matches" in error for error in errors))

    def test_valid_problem_without_exact_replacement_fields_is_supported(self) -> None:
        page = "## Description\n\nSee Sect. 2.1. first. See Sect. 2.1. again.\n"
        report = self.report()

        self.assertEqual(self.validate(report, page), [])

    def test_main_removes_ambiguous_fields_before_writing_publishable_output(
        self,
    ) -> None:
        page = "## Description\n\nSee Sect. 2.1. first. See Sect. 2.1. again.\n"
        report = self.report(current_text="Sect. 2.1.", proposed_text="Section 2.1.")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prompt_path = root / "prompt.md"
            page_path = root / "docs/stereotypes/classes/example.md"
            output_path = root / "output.md"
            prompt_path.write_text("Prompt", encoding="utf-8")
            page_path.parent.mkdir(parents=True)
            page_path.write_text(page, encoding="utf-8")
            args = argparse.Namespace(
                agent="language-style-checker",
                page="docs/stereotypes/classes/example.md",
                provider="gemini",
                model="test-model",
                output="output.md",
                prompt="prompt.md",
                prompt_id="language-style-checker-v1.0.3",
                commit_sha="abc123",
                review_date="2026-07-11",
                max_completion_tokens=3000,
            )
            provider = mock.Mock(return_value=report)

            with (
                mock.patch.object(check_agent, "parse_args", return_value=args),
                mock.patch.object(check_agent, "get_repo_root", return_value=root),
                mock.patch.object(
                    check_agent,
                    "require_executable_slot",
                    return_value=mock.Mock(
                        agents=("language-style-checker",),
                        spec="gemini:test-model",
                        max_completion_tokens=3000,
                    ),
                ),
                mock.patch.object(check_agent, "load_provider", return_value=provider),
            ):
                result = check_agent.main()

            written = output_path.read_text(encoding="utf-8")
            invalid_exists = output_path.with_suffix(".invalid.md").exists()

        self.assertEqual(result, 0)
        self.assertIn("#### S-001 — Abbreviated section label", written)
        self.assertNotIn("current_text", written)
        self.assertNotIn("proposed_text", written)
        self.assertFalse(invalid_exists)

    def test_main_removes_unquoted_placeholder_pair_for_grounded_signal(self) -> None:
        page = "## Description\n\nSee Sect. 2.1. for details.\n"
        report = self.report(current_text="None", proposed_text="N/A")
        report = report.replace('- current_text: "None"', "- current_text: None")
        report = report.replace('- proposed_text: "N/A"', "- proposed_text: N/A")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prompt_path = root / "prompt.md"
            page_path = root / "docs/stereotypes/classes/example.md"
            output_path = root / "output.md"
            prompt_path.write_text("Prompt", encoding="utf-8")
            page_path.parent.mkdir(parents=True)
            page_path.write_text(page, encoding="utf-8")
            args = argparse.Namespace(
                agent="language-style-checker",
                page="docs/stereotypes/classes/example.md",
                provider="gemini",
                model="test-model",
                output="output.md",
                prompt="prompt.md",
                prompt_id="language-style-checker-v1.0.3",
                commit_sha="abc123",
                review_date="2026-07-11",
                max_completion_tokens=3000,
            )

            with (
                mock.patch.object(check_agent, "parse_args", return_value=args),
                mock.patch.object(check_agent, "get_repo_root", return_value=root),
                mock.patch.object(
                    check_agent,
                    "require_executable_slot",
                    return_value=mock.Mock(
                        agents=("language-style-checker",),
                        spec="gemini:test-model",
                        max_completion_tokens=3000,
                    ),
                ),
                mock.patch.object(check_agent, "load_provider", return_value=mock.Mock(return_value=report)),
            ):
                result = check_agent.main()

            written = output_path.read_text(encoding="utf-8")
            invalid_exists = output_path.with_suffix(".invalid.md").exists()

        self.assertEqual(result, 0)
        self.assertNotIn("current_text", written)
        self.assertNotIn("proposed_text", written)
        self.assertFalse(invalid_exists)

    def test_main_rejects_ungrounded_signal_with_unquoted_placeholder_pair(self) -> None:
        page = "## Description\n\nCurrent wording.\n"
        report = self.report(current_text="None", proposed_text="N/A")
        report = report.replace('- current_text: "None"', "- current_text: None")
        report = report.replace('- proposed_text: "N/A"', "- proposed_text: N/A")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prompt_path = root / "prompt.md"
            page_path = root / "docs/stereotypes/classes/example.md"
            output_path = root / "output.md"
            invalid_path = output_path.with_suffix(".invalid.md")
            prompt_path.write_text("Prompt", encoding="utf-8")
            page_path.parent.mkdir(parents=True)
            page_path.write_text(page, encoding="utf-8")
            args = argparse.Namespace(
                agent="language-style-checker",
                page="docs/stereotypes/classes/example.md",
                provider="gemini",
                model="test-model",
                output="output.md",
                prompt="prompt.md",
                prompt_id="language-style-checker-v1.0.3",
                commit_sha="abc123",
                review_date="2026-07-11",
                max_completion_tokens=3000,
            )

            with (
                mock.patch.object(check_agent, "parse_args", return_value=args),
                mock.patch.object(check_agent, "get_repo_root", return_value=root),
                mock.patch.object(
                    check_agent,
                    "require_executable_slot",
                    return_value=mock.Mock(
                        agents=("language-style-checker",),
                        spec="gemini:test-model",
                        max_completion_tokens=3000,
                    ),
                ),
                mock.patch.object(check_agent, "load_provider", return_value=mock.Mock(return_value=report)),
            ):
                result = check_agent.main()

            invalid_text = invalid_path.read_text(encoding="utf-8")
            output_exists = output_path.exists()

        self.assertEqual(result, 1)
        self.assertFalse(output_exists)
        self.assertIn("- current_text: None", invalid_text)
        self.assertIn("- proposed_text: N/A", invalid_text)

    def test_main_rejects_placeholder_pair_when_whitespace_normalization_would_create_grounding(self) -> None:
        page = "## Description\n\nSee Sect. 2.1. for details.\n"
        report = self.report(
            current_text="None",
            proposed_text="N/A",
            location_fragment="See  Sect. 2.1. for details.",
        )
        report = report.replace('- current_text: "None"', "- current_text: None")
        report = report.replace('- proposed_text: "N/A"', "- proposed_text: N/A")

        result, output_text, invalid_text = self.run_main_with_report(page=page, report=report)

        self.assertEqual(result, 1)
        self.assertIsNone(output_text)
        self.assertIsNotNone(invalid_text)
        self.assertIn("- current_text: None", invalid_text or "")
        self.assertIn("- proposed_text: N/A", invalid_text or "")

    def test_main_rejects_zero_match_pair_when_whitespace_normalization_would_create_grounding(self) -> None:
        page = "## Description\n\nSee Sect. 2.1. for details.\n"
        report = self.report(
            current_text="Missing target.",
            proposed_text="Replacement.",
            location_fragment="See  Sect. 2.1. for details.",
        )

        result, output_text, invalid_text = self.run_main_with_report(page=page, report=report)

        self.assertEqual(result, 1)
        self.assertIsNone(output_text)
        self.assertIsNotNone(invalid_text)
        self.assertIn('- current_text: "Missing target."', invalid_text or "")
        self.assertIn('- proposed_text: "Replacement."', invalid_text or "")

    def test_main_rejects_placeholder_pair_when_truncation_would_create_grounding(self) -> None:
        grounded_prefix = "A" * check_agent.MAX_LOCATION_FRAGMENT_CHARS
        page = f"## Description\n\n{grounded_prefix}\n"
        report = self.report(
            current_text="None",
            proposed_text="N/A",
            location_fragment=f"{grounded_prefix} FABRICATED",
        )
        report = report.replace('- current_text: "None"', "- current_text: None")
        report = report.replace('- proposed_text: "N/A"', "- proposed_text: N/A")

        result, output_text, invalid_text = self.run_main_with_report(page=page, report=report)

        self.assertEqual(result, 1)
        self.assertIsNone(output_text)
        self.assertIsNotNone(invalid_text)
        self.assertIn("- current_text: None", invalid_text or "")
        self.assertIn("- proposed_text: N/A", invalid_text or "")

    def test_main_rejects_zero_match_pair_when_truncation_would_create_grounding(self) -> None:
        grounded_prefix = "A" * check_agent.MAX_LOCATION_FRAGMENT_CHARS
        page = f"## Description\n\n{grounded_prefix}\n"
        report = self.report(
            current_text="Missing target.",
            proposed_text="Replacement.",
            location_fragment=f"{grounded_prefix} FABRICATED",
        )

        result, output_text, invalid_text = self.run_main_with_report(page=page, report=report)

        self.assertEqual(result, 1)
        self.assertIsNone(output_text)
        self.assertIsNotNone(invalid_text)
        self.assertIn('- current_text: "Missing target."', invalid_text or "")
        self.assertIn('- proposed_text: "Replacement."', invalid_text or "")

    def test_full_page_is_used_for_uniqueness_not_only_scoped_reader_content(
        self,
    ) -> None:
        full_page = "## Description\n\nSee Sect. 2.1. for details.\n\n## References\n\nA source mentioning Sect. 2.1.\n"
        report = self.report(current_text="Sect. 2.1.", proposed_text="Section 2.1.")

        normalized, messages = check_agent.strip_ambiguous_exact_replacement_fields(report, full_page)

        self.assertEqual(len(messages), 1)
        self.assertNotIn("current_text", normalized)
        self.assertEqual(self.validate(normalized, full_page), [])


class ResolverExactReplacementTests(unittest.TestCase):
    PAGE = "docs/stereotypes/classes/example.md"

    def make_issue(self, number: int = 300) -> resolver.IssueSnapshot:
        return resolver.IssueSnapshot(
            number=number,
            title="Check signal: language-style-checker: classes/example",
            body="",
            state="OPEN",
            url=f"https://github.com/example/repository/issues/{number}",
            agent="language-style-checker",
            reviewed_page=self.PAGE,
            comments=[],
        )

    def edit(self, current: str, proposed: str) -> dict[str, str]:
        return {
            "current_text": current,
            "proposed_text": proposed,
            "rationale": "The edit is local, deterministic, and meaning-preserving.",
        }

    def group(self, group_id: str, edits: list[dict[str, str]]) -> dict[str, object]:
        return {
            "group_id": group_id,
            "source_signal_refs": [f"comment 1 {group_id}"],
            "decision": "accept",
            "reason_code": "in_scope_exact_edit",
            "rationale": "The reported language issue has an exact local repair.",
            "edits": edits,
        }

    def plan(self, groups: list[dict[str, object]], *, number: int = 300) -> dict[str, object]:
        return {
            "issue_number": number,
            "agent": "language-style-checker",
            "reviewed_page": self.PAGE,
            "overall_decision": "accepted_changes",
            "signal_groups": groups,
            "issue_comment": "Accepted edits are available at {{PR_URL}}.",
        }

    def page_with_log(self, body: str) -> str:
        return (
            f"## Description\n\n{body}\n\n"
            "## Generation and Review Log\n\n"
            "| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |\n"
            "|---|---|---|---|---|---|---|---|\n"
        )

    def test_unique_edit_remains_accepted(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Old wording.", "New wording.")])])
        page = "Old wording.\n"

        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)

        self.assertEqual(records, [])
        self.assertEqual(plan["signal_groups"][0]["decision"], "accept")
        resolver.validate_plan(plan, issue, page)

    def test_multiple_occurrences_can_use_independently_identifiable_edits_in_one_group(
        self,
    ) -> None:
        issue = self.make_issue()
        first = "First locator uses Sect. 2.1."
        second = "Second locator uses Sect. 2.1."
        plan = self.plan(
            [
                self.group(
                    "G-001",
                    [
                        self.edit(first, "First locator uses Section 2.1."),
                        self.edit(second, "Second locator uses Section 2.1."),
                    ],
                )
            ]
        )
        page = self.page_with_log(f"{first}\n\n{second}")

        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)
        updated = resolver.apply_edits(page, plan)

        self.assertEqual(records, [])
        self.assertIn("First locator uses Section 2.1.", updated)
        self.assertIn("Second locator uses Section 2.1.", updated)
        self.assertNotIn("uses Sect. 2.1.", updated)

    def test_positional_application_is_not_redirected_by_text_introduced_by_an_earlier_edit(
        self,
    ) -> None:
        issue = self.make_issue()
        plan = self.plan(
            [
                self.group(
                    "G-001",
                    [
                        self.edit("Alpha.", "Beta."),
                        self.edit("Beta.", "Gamma."),
                    ],
                )
            ]
        )
        page = self.page_with_log("Alpha. Beta.")

        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)
        updated = resolver.apply_edits(page, plan)

        self.assertEqual(records, [])
        self.assertIn("Beta. Gamma.", updated)
        self.assertNotIn("Gamma. Beta.", updated)

    def test_semantic_placeholder_proposed_values_demote_atomic_group(self) -> None:
        issue = self.make_issue()
        for placeholder in ("None", "N/A", "Not applicable"):
            with self.subTest(placeholder=placeholder):
                plan = self.plan([self.group("G-001", [self.edit("Old wording.", placeholder)])])
                page = "Old wording.\n"

                records = resolver.demote_invalid_accepted_groups(plan, issue, page)
                resolver.normalize_overall_decision(plan)
                resolver.validate_plan(plan, issue, page)

                self.assertEqual(len(records), 1)
                self.assertEqual(plan["signal_groups"][0]["decision"], "reject_for_phase_2_automation")
                self.assertEqual(plan["signal_groups"][0]["reason_code"], "unsafe_edit")
                self.assertIn("recognized placeholder value", plan["signal_groups"][0]["rationale"])

    def test_semantic_placeholder_current_text_demotes_atomic_group_even_when_it_matches(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("None", "Replacement.")])])
        page = "None\n"

        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)

        self.assertEqual(len(records), 1)
        self.assertEqual(plan["signal_groups"][0]["decision"], "reject_for_phase_2_automation")
        self.assertEqual(plan["signal_groups"][0]["reason_code"], "unsafe_edit")
        self.assertIn("current_text is a recognized placeholder value", plan["signal_groups"][0]["rationale"])

    def test_placeholder_edit_demotes_complete_group_but_preserves_independent_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan(
            [
                self.group(
                    "G-001",
                    [
                        self.edit("Old wording.", "New wording."),
                        self.edit("Another old phrase.", "N/A"),
                    ],
                ),
                self.group("G-002", [self.edit("Independent old phrase.", "Independent new phrase.")]),
            ]
        )
        page = "Old wording.\nAnother old phrase.\nIndependent old phrase.\n"

        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)

        self.assertEqual(len(records), 1)
        self.assertEqual(plan["signal_groups"][0]["decision"], "reject_for_phase_2_automation")
        self.assertEqual(plan["signal_groups"][0]["edits"], [])
        self.assertEqual(plan["signal_groups"][1]["decision"], "accept")
        self.assertEqual(plan["overall_decision"], "accepted_changes")

    def test_final_validation_rejects_semantic_placeholder_if_revalidation_is_bypassed(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Old wording.", "None")])])

        with self.assertRaisesRegex(resolver.ResolverError, "recognized placeholder values"):
            resolver.validate_plan(plan, issue, "Old wording.\n")

    def test_unchanged_edit_demotes_atomic_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Old wording.", "Old wording.")])])

        records = resolver.demote_invalid_accepted_groups(plan, issue, "Old wording.\n")
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, "Old wording.\n")

        self.assertEqual(len(records), 1)
        self.assertEqual(plan["signal_groups"][0]["decision"], "reject_for_phase_2_automation")
        self.assertEqual(plan["signal_groups"][0]["reason_code"], "unsafe_edit")
        self.assertIn("identical current_text and proposed_text", plan["signal_groups"][0]["rationale"])

    def test_duplicate_targets_across_groups_demote_both_groups(self) -> None:
        issue = self.make_issue()
        plan = self.plan(
            [
                self.group("G-001", [self.edit("Old wording.", "First replacement.")]),
                self.group("G-002", [self.edit("Old wording.", "Second replacement.")]),
            ]
        )

        records = resolver.demote_invalid_accepted_groups(plan, issue, "Old wording.\n")
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, "Old wording.\n")

        self.assertEqual(len(records), 2)
        self.assertTrue(all(group["decision"] == "reject_for_phase_2_automation" for group in plan["signal_groups"]))
        self.assertTrue(all(group["edits"] == [] for group in plan["signal_groups"]))
        self.assertEqual(plan["overall_decision"], "no_accepted_changes")

    def test_cross_group_overlap_demotes_both_otherwise_valid_groups(self) -> None:
        issue = self.make_issue()
        plan = self.plan(
            [
                self.group("G-001", [self.edit("ABC", "First replacement")]),
                self.group("G-002", [self.edit("BCD", "Second replacement")]),
            ]
        )

        records = resolver.demote_invalid_accepted_groups(plan, issue, "ABCDE\n")
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, "ABCDE\n")

        self.assertEqual(len(records), 2)
        self.assertTrue(all(group["decision"] == "reject_for_phase_2_automation" for group in plan["signal_groups"]))
        self.assertTrue(all(group["edits"] == [] for group in plan["signal_groups"]))
        self.assertEqual(plan["overall_decision"], "no_accepted_changes")

    def test_zero_match_demotes_only_affected_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Missing text.", "Replacement.")])])

        records = resolver.demote_invalid_accepted_groups(plan, issue, "Current text.\n")
        resolver.normalize_overall_decision(plan)

        group = plan["signal_groups"][0]
        self.assertEqual(len(records), 1)
        self.assertEqual(group["decision"], "reject_for_phase_2_automation")
        self.assertEqual(group["reason_code"], "no_current_page_match")
        self.assertEqual(group["edits"], [])
        self.assertEqual(plan["overall_decision"], "no_accepted_changes")
        self.assertNotIn("{{PR_URL}}", plan["issue_comment"])
        self.assertIn("No page changes were applied", plan["issue_comment"])
        resolver.validate_plan(plan, issue, "Current text.\n")

    def test_unintended_multiple_matches_demote_affected_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Sect.", "Section")])])

        records = resolver.demote_invalid_accepted_groups(plan, issue, "Sect. one. Sect. two.\n")
        resolver.normalize_overall_decision(plan)

        group = plan["signal_groups"][0]
        self.assertEqual(len(records), 1)
        self.assertEqual(group["decision"], "reject_for_phase_2_automation")
        self.assertEqual(group["reason_code"], "not_deterministic_or_local")
        self.assertIn("2 matches", group["rationale"])
        resolver.validate_plan(plan, issue, "Sect. one. Sect. two.\n")

    def test_whitespace_only_current_text_demotes_affected_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("   ", "replacement")])])

        resolver.validate_plan_structure_before_revalidation(plan, issue)
        records = resolver.demote_invalid_accepted_groups(plan, issue, "A   B\n")
        resolver.normalize_overall_decision(plan)

        group = plan["signal_groups"][0]
        self.assertEqual(len(records), 1)
        self.assertEqual(group["decision"], "reject_for_phase_2_automation")
        self.assertIn("no non-empty current_text", group["rationale"])
        resolver.validate_plan(plan, issue, "A   B\n")

    def test_empty_proposed_text_demotes_affected_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Old wording.", "")])])

        resolver.validate_plan_structure_before_revalidation(plan, issue)
        records = resolver.demote_invalid_accepted_groups(plan, issue, "Old wording.\n")
        resolver.normalize_overall_decision(plan)

        group = plan["signal_groups"][0]
        self.assertEqual(len(records), 1)
        self.assertEqual(group["decision"], "reject_for_phase_2_automation")
        self.assertEqual(group["reason_code"], "not_deterministic_or_local")
        self.assertIn("no non-empty proposed_text", group["rationale"])
        resolver.validate_plan(plan, issue, "Old wording.\n")

    def test_overlapping_matches_demote_affected_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("aaa", "bbb")])])

        records = resolver.demote_invalid_accepted_groups(plan, issue, "aaaa\n")
        resolver.normalize_overall_decision(plan)

        group = plan["signal_groups"][0]
        self.assertEqual(len(records), 1)
        self.assertEqual(group["decision"], "reject_for_phase_2_automation")
        self.assertIn("2 matches", group["rationale"])
        resolver.validate_plan(plan, issue, "aaaa\n")

    def test_one_invalid_group_does_not_remove_another_valid_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan(
            [
                self.group("G-001", [self.edit("Missing text.", "Replacement.")]),
                self.group("G-002", [self.edit("Old wording.", "New wording.")]),
            ]
        )
        page = "Old wording.\n"

        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)

        self.assertEqual(len(records), 1)
        self.assertEqual(plan["signal_groups"][0]["decision"], "reject_for_phase_2_automation")
        self.assertEqual(plan["signal_groups"][1]["decision"], "accept")
        self.assertEqual(plan["overall_decision"], "accepted_changes")
        self.assertIn("{{PR_URL}}", plan["issue_comment"])
        self.assertIn("Automatic deterministic rejections", plan["issue_comment"])
        self.assertIn(
            "A pull request with the accepted deterministic local language/style edits is available here: {{PR_URL}}",
            plan["issue_comment"],
        )
        self.assertIn(
            "The pull request applies only the remaining deterministic local Phase 2 language/style edits.",
            plan["issue_comment"],
        )

    def test_automatic_rejection_comment_preserves_page_hygiene_pr_contract(
        self,
    ) -> None:
        issue = resolver.IssueSnapshot(
            number=300,
            title="Check signal: page-hygiene-checker: classes/example",
            body="",
            state="OPEN",
            url="https://github.com/example/repository/issues/300",
            agent="page-hygiene-checker",
            reviewed_page=self.PAGE,
            comments=[],
        )
        plan = self.plan(
            [
                self.group("G-001", [self.edit("Missing text.", "Replacement.")]),
                self.group("G-002", [self.edit("Old wording.", "New wording.")]),
            ]
        )
        plan["agent"] = "page-hygiene-checker"
        page = "Old wording.\n"

        resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)

        self.assertIn(
            "A pull request with the accepted deterministic local page-hygiene edits is available here: {{PR_URL}}",
            plan["issue_comment"],
        )
        self.assertIn(
            "The pull request applies only the remaining deterministic local Phase 2 page-hygiene edits.",
            plan["issue_comment"],
        )

    def test_issue_comment_distinguishes_automatic_and_explicit_rejections(
        self,
    ) -> None:
        issue = self.make_issue()
        explicit = {
            "group_id": "G-002",
            "source_signal_refs": ["comment 2 S-002"],
            "decision": "reject_for_phase_2_automation",
            "reason_code": "out_of_scope",
            "rationale": "The signal is outside the language-style resolver scope.",
            "edits": [],
        }
        plan = self.plan(
            [
                self.group("G-001", [self.edit("Missing text.", "Replacement.")]),
                explicit,
            ]
        )

        resolver.demote_invalid_accepted_groups(plan, issue, "Current text.\n")
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, "Current text.\n")

        comment = plan["issue_comment"]
        self.assertIn("Automatic deterministic rejections", comment)
        self.assertIn("Resolver rejections", comment)
        self.assertIn("G-001", comment)
        self.assertIn("G-002", comment)
        self.assertIn("explicitly rejected during normal resolution", comment)

    def test_one_invalid_edit_demotes_its_complete_atomic_group(self) -> None:
        issue = self.make_issue()
        plan = self.plan(
            [
                self.group(
                    "G-001",
                    [
                        self.edit("Old wording.", "New wording."),
                        self.edit("Missing text.", "Replacement."),
                    ],
                ),
                self.group("G-002", [self.edit("Another old phrase.", "Another new phrase.")]),
            ]
        )
        page = "Old wording.\nAnother old phrase.\n"

        resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)

        self.assertEqual(plan["signal_groups"][0]["decision"], "reject_for_phase_2_automation")
        self.assertEqual(plan["signal_groups"][0]["edits"], [])
        self.assertEqual(plan["signal_groups"][1]["decision"], "accept")

    def test_internally_overlapping_group_does_not_demote_independent_group(
        self,
    ) -> None:
        issue = self.make_issue()
        plan = self.plan(
            [
                self.group(
                    "G-001",
                    [
                        self.edit("ABC", "First replacement"),
                        self.edit("BCD", "Second replacement"),
                    ],
                ),
                self.group("G-002", [self.edit("CDE", "Valid replacement")]),
            ]
        )
        page = "ABCDE\n"

        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["group_id"], "G-001")
        self.assertEqual(
            plan["signal_groups"][0]["decision"],
            "reject_for_phase_2_automation",
        )
        self.assertEqual(plan["signal_groups"][1]["decision"], "accept")
        self.assertEqual(plan["overall_decision"], "accepted_changes")

    def test_malformed_edit_shape_demotes_only_its_atomic_group(self) -> None:
        issue = self.make_issue()
        malformed = self.group("G-001", [])
        malformed["edits"] = [
            {
                "current_text": "Old wording.",
                "proposed_text": "New wording.",
            }
        ]
        valid = self.group("G-002", [self.edit("Another old phrase.", "Another new phrase.")])
        plan = self.plan([malformed, valid])
        page = "Old wording.\nAnother old phrase.\n"

        resolver.validate_plan_structure_before_revalidation(plan, issue)
        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)

        self.assertEqual(len(records), 1)
        self.assertEqual(plan["signal_groups"][0]["decision"], "reject_for_phase_2_automation")
        self.assertIn("no non-empty rationale", plan["signal_groups"][0]["rationale"])
        self.assertEqual(plan["signal_groups"][1]["decision"], "accept")

    def test_malformed_edit_array_demotes_only_its_atomic_group(self) -> None:
        issue = self.make_issue()
        malformed = self.group("G-001", [])
        malformed["edits"] = {"current_text": "Old wording."}
        valid = self.group("G-002", [self.edit("Another old phrase.", "Another new phrase.")])
        plan = self.plan([malformed, valid])
        page = "Old wording.\nAnother old phrase.\n"

        resolver.validate_plan_structure_before_revalidation(plan, issue)
        records = resolver.demote_invalid_accepted_groups(plan, issue, page)
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, page)

        self.assertEqual(len(records), 1)
        self.assertEqual(plan["signal_groups"][0]["decision"], "reject_for_phase_2_automation")
        self.assertIn(
            "does not contain a non-empty edits array",
            plan["signal_groups"][0]["rationale"],
        )
        self.assertEqual(plan["signal_groups"][1]["decision"], "accept")

    def test_empty_source_signal_refs_remain_fail_closed(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Old wording.", "New wording.")])])
        plan["signal_groups"][0]["source_signal_refs"] = []

        with self.assertRaisesRegex(resolver.ResolverError, "non-empty source_signal_refs"):
            resolver.validate_plan_structure_before_revalidation(plan, issue)

        with self.assertRaisesRegex(resolver.ResolverError, "non-empty source_signal_refs"):
            resolver.validate_plan(plan, issue, "Old wording.\n")

    def test_schema_error_is_not_concealed_by_invalid_target_demotion(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Missing text.", "Replacement.")])])
        plan["signal_groups"][0]["reason_code"] = "unsupported_reason"

        with self.assertRaisesRegex(resolver.ResolverError, "Invalid reason_code"):
            resolver.validate_plan_structure_before_revalidation(plan, issue)

    def test_stale_issue_comment_placeholder_does_not_block_group_local_demotion(
        self,
    ) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Missing text.", "Replacement.")])])
        plan["overall_decision"] = "no_accepted_changes"
        plan["issue_comment"] = "No accepted changes were reported by the resolver."

        resolver.validate_plan_structure_before_revalidation(plan, issue)
        records = resolver.demote_invalid_accepted_groups(plan, issue, "Current text.\n")
        resolver.normalize_overall_decision(plan)
        resolver.validate_plan(plan, issue, "Current text.\n")

        self.assertEqual(len(records), 1)
        self.assertNotIn("{{PR_URL}}", plan["issue_comment"])
        self.assertIn("No page changes were applied", plan["issue_comment"])

    def test_missing_pr_placeholder_still_fails_when_no_group_is_demoted(self) -> None:
        issue = self.make_issue()
        plan = self.plan([self.group("G-001", [self.edit("Old wording.", "New wording.")])])
        plan["issue_comment"] = "Accepted edits are available."

        resolver.validate_plan_structure_before_revalidation(plan, issue)
        records = resolver.demote_invalid_accepted_groups(plan, issue, "Old wording.\n")
        resolver.normalize_overall_decision(plan)

        self.assertEqual(records, [])
        with self.assertRaisesRegex(resolver.ResolverError, r"must contain \{\{PR_URL\}\}"):
            resolver.validate_plan(plan, issue, "Old wording.\n")

    def test_main_fails_closed_on_schema_error_before_target_demotion(self) -> None:
        issue = self.make_issue(303)
        plan = self.plan(
            [self.group("G-001", [self.edit("Missing text.", "Replacement.")])],
            number=303,
        )
        plan["signal_groups"][0]["reason_code"] = "unsupported_reason"
        args = argparse.Namespace(
            repo="example/repository",
            issue="303",
            provider="gemini",
            model="gemini-3.5-flash",
            max_completion_tokens=8000,
            provider_max_attempts=1,
            dry_run=False,
            branch_prefix="phase-2/auto-resolve",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "artifacts"
            output_dir.mkdir()
            previous_cwd = Path.cwd()
            os.chdir(tmpdir)
            try:
                with (
                    mock.patch.object(resolver, "parse_args", return_value=args),
                    mock.patch.object(resolver, "read_issue", return_value=issue),
                    mock.patch.object(
                        resolver,
                        "load_text",
                        side_effect=lambda path: "Current text.\n" if str(path) == issue.reviewed_page else "prompt",
                    ),
                    mock.patch.object(resolver, "resolver_output_dir", return_value=output_dir),
                    mock.patch.object(resolver, "call_provider", return_value=json.dumps(plan)),
                    mock.patch.object(resolver, "comment_and_close") as close,
                    mock.patch.object(resolver, "create_pr") as create_pr,
                ):
                    result = resolver.main()
                automatic_rejections_exists = (output_dir / "issue-303-automatic-rejections.json").exists()
                plan_error = (output_dir / "issue-303-plan-error.txt").read_text(encoding="utf-8")
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(result, 1)
        create_pr.assert_not_called()
        close.assert_not_called()
        self.assertFalse(automatic_rejections_exists)
        self.assertIn("Invalid reason_code", plan_error)

    def test_main_closes_not_planned_without_modifying_page_when_nothing_remains(
        self,
    ) -> None:
        issue = self.make_issue(301)
        plan = self.plan(
            [self.group("G-001", [self.edit("Missing text.", "Replacement.")])],
            number=301,
        )
        args = argparse.Namespace(
            repo="example/repository",
            issue="301",
            provider="gemini",
            model="gemini-3.5-flash",
            max_completion_tokens=8000,
            provider_max_attempts=1,
            dry_run=False,
            branch_prefix="phase-2/auto-resolve",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "artifacts"
            output_dir.mkdir()
            page_path = Path(tmpdir) / issue.reviewed_page
            page_path.parent.mkdir(parents=True)
            original_page = "Current text.\n"
            page_path.write_text(original_page, encoding="utf-8")
            previous_cwd = Path.cwd()
            os.chdir(tmpdir)
            try:
                with (
                    mock.patch.object(resolver, "parse_args", return_value=args),
                    mock.patch.object(resolver, "read_issue", return_value=issue),
                    mock.patch.object(
                        resolver,
                        "load_text",
                        side_effect=lambda path: (
                            page_path.read_text(encoding="utf-8")
                            if Path(path) == Path(issue.reviewed_page)
                            else "prompt"
                        ),
                    ),
                    mock.patch.object(resolver, "resolver_output_dir", return_value=output_dir),
                    mock.patch.object(resolver, "call_provider", return_value=json.dumps(plan)),
                    mock.patch.object(resolver, "comment_and_close") as close,
                    mock.patch.object(resolver, "create_pr") as create_pr,
                ):
                    result = resolver.main()
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(page_path.read_text(encoding="utf-8"), original_page)

        self.assertEqual(result, 0)
        create_pr.assert_not_called()
        close.assert_called_once()
        self.assertEqual(close.call_args.args[3], "not_planned")
        self.assertIn("No page changes were applied", close.call_args.args[2])
        self.assertIn("closed as not planned", close.call_args.args[2])
        self.assertIn("not necessarily false", close.call_args.args[2])
        self.assertIn("did not perform source-faithfulness validation", close.call_args.args[2])
        self.assertIn("Automatic deterministic rejections", close.call_args.args[2])

    def test_main_applies_valid_group_and_records_automatic_rejection(self) -> None:
        issue = self.make_issue(302)
        plan = self.plan(
            [
                self.group("G-001", [self.edit("Missing text.", "Replacement.")]),
                self.group("G-002", [self.edit("Old wording.", "New wording.")]),
            ],
            number=302,
        )
        args = argparse.Namespace(
            repo="example/repository",
            issue="302",
            provider="gemini",
            model="gemini-3.5-flash",
            max_completion_tokens=8000,
            provider_max_attempts=1,
            dry_run=False,
            branch_prefix="phase-2/auto-resolve",
        )
        page = self.page_with_log("Old wording.")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page_path = root / issue.reviewed_page
            page_path.parent.mkdir(parents=True)
            page_path.write_text(page, encoding="utf-8")
            output_dir = root / "artifacts"
            output_dir.mkdir()
            previous_cwd = Path.cwd()
            os.chdir(root)
            try:
                with (
                    mock.patch.object(resolver, "parse_args", return_value=args),
                    mock.patch.object(resolver, "read_issue", return_value=issue),
                    mock.patch.object(
                        resolver,
                        "load_text",
                        side_effect=lambda path: (
                            page_path.read_text(encoding="utf-8")
                            if Path(path) == Path(issue.reviewed_page)
                            else "prompt"
                        ),
                    ),
                    mock.patch.object(resolver, "resolver_output_dir", return_value=output_dir),
                    mock.patch.object(resolver, "call_provider", return_value=json.dumps(plan)),
                    mock.patch.object(resolver, "run_structure_check"),
                    mock.patch.object(
                        resolver,
                        "create_pr",
                        return_value="https://example.invalid/pr/1",
                    ),
                    mock.patch.object(resolver, "update_pr_branch"),
                    mock.patch.object(resolver, "enable_pr_auto_merge"),
                    mock.patch.object(resolver, "comment_and_close") as close,
                ):
                    result = resolver.main()
                updated = page_path.read_text(encoding="utf-8")
                auto_artifact = json.loads(
                    (output_dir / "issue-302-automatic-rejections.json").read_text(encoding="utf-8")
                )
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(result, 0)
        self.assertIn("New wording.", updated)
        self.assertNotIn("Old wording.", updated)
        self.assertEqual(len(auto_artifact), 1)
        close.assert_called_once()
        self.assertEqual(close.call_args.args[3], "completed")
        self.assertIn("https://example.invalid/pr/1", close.call_args.args[2])
        self.assertIn("Automatic deterministic rejections", close.call_args.args[2])
        self.assertIn(
            "The pull request applies only the remaining deterministic local Phase 2 language/style edits.",
            close.call_args.args[2],
        )
        self.assertIn("not necessarily false", close.call_args.args[2])
        self.assertIn("did not perform source-faithfulness validation", close.call_args.args[2])
        self.assertIn("G-001", close.call_args.args[2])


if __name__ == "__main__":
    unittest.main()
