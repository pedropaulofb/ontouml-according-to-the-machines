#!/usr/bin/env python3
"""Run a Phase 2 batch of page-review generations and issue postings.

This script orchestrates the existing Phase 2 scripts:

- scripts/phase-2/run_page_review.py
- scripts/phase-2/issue_manager.py

It does not call LLM providers directly and does not implement GitHub issue
logic directly. It delegates those responsibilities to the existing scripts.

Typical flow with post_mode=after_page:

for each page:
    for each model:
        run_page_review.py -> generated candidate comment
    for each generated candidate comment:
        issue_manager.py -> post comment to deterministic page-level issue

The script is designed to run locally first and later from GitHub Actions.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUPPORTED_POST_MODES = {"after_page", "after_each_model", "none"}


class BatchReviewError(RuntimeError):
    """Raised when the batch configuration or execution is invalid."""


@dataclass(frozen=True)
class ModelConfig:
    """One reviewer-model configuration."""

    provider: str
    model: str
    slug: str
    max_completion_tokens: int


@dataclass(frozen=True)
class BatchConfig:
    """Normalized batch configuration."""

    repo: str
    output_dir: Path
    delay_seconds: int
    continue_on_error: bool
    post_mode: str
    post_empty: bool
    labels: list[str]
    models: list[ModelConfig]
    pages: list[str]


@dataclass(frozen=True)
class GeneratedComment:
    """Generated candidate comment for a page/model run."""

    page: str
    model: ModelConfig
    path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a configured Phase 2 page-review batch."
    )

    parser.add_argument(
        "--config",
        default="configs/phase-2/review-batch.yml",
        help="Path to the Phase 2 batch YAML configuration file.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned commands without executing them.",
    )

    parser.add_argument(
        "--only-page",
        default=None,
        help=(
            "Optional page path filter. When provided, only this page from the "
            "configuration is processed."
        ),
    )

    parser.add_argument(
        "--only-model",
        default=None,
        help=(
            "Optional model slug or model name filter. When provided, only this "
            "model from the configuration is processed."
        ),
    )

    parser.add_argument(
        "--delay-seconds",
        type=int,
        default=None,
        help="Override delay_seconds from the configuration.",
    )

    parser.add_argument(
        "--no-post",
        action="store_true",
        help="Generate local candidate comments only; do not post to GitHub issues.",
    )

    parser.add_argument(
        "--post-empty",
        action="store_true",
        help=(
            "Override the configuration and allow issue_manager.py to create/post "
            "even when Finding count is 0 and no issue exists."
        ),
    )

    return parser.parse_args()


def get_repo_root() -> Path:
    """Return the repository root based on this script's location."""
    return Path(__file__).resolve().parents[2]


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML configuration file."""
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as exc:
        raise BatchReviewError(
            "PyYAML is required to read review-batch.yml. "
            "Install it with: python -m pip install pyyaml"
        ) from exc

    if not path.exists():
        raise BatchReviewError(f"Configuration file does not exist: {path}")

    if not path.is_file():
        raise BatchReviewError(f"Configuration path is not a file: {path}")

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise BatchReviewError(f"Failed to parse YAML configuration: {path}") from exc

    if not isinstance(raw, dict):
        raise BatchReviewError("Configuration root must be a YAML mapping.")

    return raw


def require_string(config: dict[str, Any], key: str) -> str:
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        raise BatchReviewError(f"Configuration key `{key}` must be a non-empty string.")
    return value.strip()


def optional_int(config: dict[str, Any], key: str, default: int) -> int:
    value = config.get(key, default)
    if not isinstance(value, int):
        raise BatchReviewError(f"Configuration key `{key}` must be an integer.")
    return value


def optional_bool(config: dict[str, Any], key: str, default: bool) -> bool:
    value = config.get(key, default)
    if not isinstance(value, bool):
        raise BatchReviewError(f"Configuration key `{key}` must be a boolean.")
    return value


def optional_string_list(config: dict[str, Any], key: str) -> list[str]:
    value = config.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise BatchReviewError(f"Configuration key `{key}` must be a list of strings.")
    return [item.strip() for item in value if item.strip()]


def load_batch_config(config_path: Path, repo_root: Path) -> BatchConfig:
    raw = load_yaml_file(config_path)

    repo = require_string(raw, "repo")
    output_dir_raw = require_string(raw, "output_dir")
    output_dir = Path(output_dir_raw)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    delay_seconds = optional_int(raw, "delay_seconds", 60)
    if delay_seconds < 0:
        raise BatchReviewError("delay_seconds must not be negative.")

    continue_on_error = optional_bool(raw, "continue_on_error", True)

    post_mode = str(raw.get("post_mode", "after_page")).strip()
    if post_mode not in SUPPORTED_POST_MODES:
        raise BatchReviewError(
            f"post_mode must be one of {sorted(SUPPORTED_POST_MODES)}, got: {post_mode}"
        )

    post_empty = optional_bool(raw, "post_empty", False)
    labels = optional_string_list(raw, "labels")

    raw_models = raw.get("models")
    if not isinstance(raw_models, list) or not raw_models:
        raise BatchReviewError("Configuration key `models` must be a non-empty list.")

    models: list[ModelConfig] = []
    for index, raw_model in enumerate(raw_models, start=1):
        if not isinstance(raw_model, dict):
            raise BatchReviewError(f"Model entry {index} must be a mapping.")

        provider = require_string(raw_model, "provider")
        model = require_string(raw_model, "model")
        slug = require_string(raw_model, "slug")
        max_completion_tokens = optional_int(raw_model, "max_completion_tokens", 3000)

        if max_completion_tokens <= 0:
            raise BatchReviewError(
                f"Model entry {index} has invalid max_completion_tokens: "
                f"{max_completion_tokens}"
            )

        models.append(
            ModelConfig(
                provider=provider,
                model=model,
                slug=slug,
                max_completion_tokens=max_completion_tokens,
            )
        )

    raw_pages = raw.get("pages")
    if not isinstance(raw_pages, list) or not raw_pages:
        raise BatchReviewError("Configuration key `pages` must be a non-empty list.")

    pages: list[str] = []
    for index, raw_page in enumerate(raw_pages, start=1):
        if not isinstance(raw_page, str) or not raw_page.strip():
            raise BatchReviewError(f"Page entry {index} must be a non-empty string.")
        pages.append(raw_page.strip())

    return BatchConfig(
        repo=repo,
        output_dir=output_dir,
        delay_seconds=delay_seconds,
        continue_on_error=continue_on_error,
        post_mode=post_mode,
        post_empty=post_empty,
        labels=labels,
        models=models,
        pages=pages,
    )


def slugify(value: str) -> str:
    """Create a filesystem-friendly slug while preserving useful identifiers."""
    value = value.replace("\\", "/")
    value = value.replace("/", "-")
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def page_identity_from_path(page_path: str) -> str:
    """Return classes-role or relations-mediation for a stereotype page path."""
    normalized = page_path.replace("\\", "/").strip()
    prefix = "docs/stereotypes/"

    if not normalized.startswith(prefix) or not normalized.endswith(".md"):
        return slugify(normalized.removesuffix(".md"))

    identity = normalized[len(prefix):-3]
    return slugify(identity)


def output_path_for(config: BatchConfig, page: str, model: ModelConfig) -> Path:
    page_slug = page_identity_from_path(page)
    provider_slug = slugify(model.provider)
    model_slug = slugify(model.slug)
    filename = f"issue-comment-{provider_slug}-{model_slug}.md"
    return config.output_dir / page_slug / filename


def build_review_command(
    *,
    repo_root: Path,
    page: str,
    model: ModelConfig,
    output_path: Path,
) -> list[str]:
    return [
        sys.executable,
        str(repo_root / "scripts/phase-2/run_page_review.py"),
        "--page",
        page,
        "--provider",
        model.provider,
        "--model",
        model.model,
        "--output",
        str(output_path),
        "--max-completion-tokens",
        str(model.max_completion_tokens),
    ]


def build_issue_manager_command(
    *,
    repo_root: Path,
    comment_path: Path,
    repo: str,
    labels: list[str],
    post_empty: bool,
) -> list[str]:
    command = [
        sys.executable,
        str(repo_root / "scripts/phase-2/issue_manager.py"),
        "--comment",
        str(comment_path),
        "--repo",
        repo,
    ]

    for label in labels:
        command.extend(["--label", label])

    if post_empty:
        command.append("--post-empty")

    return command


def quote_arg(value: str) -> str:
    if not value:
        return '""'
    if re.search(r"\s", value):
        return f'"{value}"'
    return value


def format_command(command: list[str]) -> str:
    return " ".join(quote_arg(part) for part in command)


def run_command(command: list[str], *, cwd: Path, dry_run: bool) -> int:
    print()
    print(format_command(command))

    if dry_run:
        return 0

    result = subprocess.run(command, cwd=cwd, check=False)
    return result.returncode


def sleep_between_steps(seconds: int, *, dry_run: bool) -> None:
    if seconds <= 0:
        return

    if dry_run:
        print(f"Would wait {seconds} second(s).")
        return

    print(f"Waiting {seconds} second(s)...")
    time.sleep(seconds)

def sleep_if_more_work(seconds: int, *, dry_run: bool, has_more_work: bool) -> None:
    """Sleep only when another batch operation remains."""
    if not has_more_work:
        return

    sleep_between_steps(seconds, dry_run=dry_run)

def should_include_page(page: str, only_page: str | None) -> bool:
    if only_page is None:
        return True
    return page.replace("\\", "/") == only_page.replace("\\", "/")


def should_include_model(model: ModelConfig, only_model: str | None) -> bool:
    if only_model is None:
        return True
    return only_model in {model.slug, model.model}


def handle_failure(message: str, *, continue_on_error: bool) -> bool:
    """Return True if the batch should continue."""
    print(f"ERROR: {message}", file=sys.stderr)
    return continue_on_error


def post_generated_comment(
    *,
    repo_root: Path,
    config: BatchConfig,
    generated: GeneratedComment,
    dry_run: bool,
    post_empty: bool,
) -> bool:
    command = build_issue_manager_command(
        repo_root=repo_root,
        comment_path=generated.path,
        repo=config.repo,
        labels=config.labels,
        post_empty=post_empty,
    )

    return_code = run_command(command, cwd=repo_root, dry_run=dry_run)

    if return_code != 0:
        return handle_failure(
            (
                "Issue manager failed for "
                f"{generated.page} / {generated.model.provider} / {generated.model.model}"
            ),
            continue_on_error=config.continue_on_error,
        )

    return True


def apply_cli_overrides(config: BatchConfig, args: argparse.Namespace) -> BatchConfig:
    delay_seconds = config.delay_seconds if args.delay_seconds is None else args.delay_seconds
    if delay_seconds < 0:
        raise BatchReviewError("--delay-seconds must not be negative.")

    post_mode = "none" if args.no_post else config.post_mode
    post_empty = config.post_empty or args.post_empty

    pages = [page for page in config.pages if should_include_page(page, args.only_page)]
    if not pages:
        raise BatchReviewError("No pages matched the selected --only-page filter.")

    models = [
        model for model in config.models if should_include_model(model, args.only_model)
    ]
    if not models:
        raise BatchReviewError("No models matched the selected --only-model filter.")

    return BatchConfig(
        repo=config.repo,
        output_dir=config.output_dir,
        delay_seconds=delay_seconds,
        continue_on_error=config.continue_on_error,
        post_mode=post_mode,
        post_empty=post_empty,
        labels=config.labels,
        models=models,
        pages=pages,
    )


def print_plan(config: BatchConfig) -> None:
    print("Phase 2 batch review plan")
    print()
    print(f"Repository: {config.repo}")
    print(f"Output directory: {config.output_dir}")
    print(f"Delay seconds: {config.delay_seconds}")
    print(f"Continue on error: {config.continue_on_error}")
    print(f"Post mode: {config.post_mode}")
    print(f"Post empty: {config.post_empty}")
    print(f"Labels: {', '.join(config.labels) if config.labels else '(none)'}")
    print()
    print("Pages:")
    for page in config.pages:
        print(f"- {page}")
    print()
    print("Models:")
    for model in config.models:
        print(
            f"- {model.provider} / {model.model} "
            f"(slug={model.slug}, max_completion_tokens={model.max_completion_tokens})"
        )


def run_batch(config: BatchConfig, *, repo_root: Path, dry_run: bool) -> int:
    failures = 0

    print_plan(config)

    for page_index, page in enumerate(config.pages, start=1):
        print()
        print("=" * 80)
        print(f"Page {page_index}/{len(config.pages)}: {page}")
        print("=" * 80)

        generated_for_page: list[GeneratedComment] = []

        for model_index, model in enumerate(config.models, start=1):
            print()
            print(
                f"Generating review {model_index}/{len(config.models)} for page: "
                f"{page} using {model.provider} / {model.model}"
            )

            output_path = output_path_for(config, page, model)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            command = build_review_command(
                repo_root=repo_root,
                page=page,
                model=model,
                output_path=output_path,
            )

            return_code = run_command(command, cwd=repo_root, dry_run=dry_run)

            if return_code != 0:
                failures += 1
                should_continue = handle_failure(
                    f"Review generation failed for {page} / {model.provider} / {model.model}",
                    continue_on_error=config.continue_on_error,
                )
                if not should_continue:
                    return 1
                continue

            generated = GeneratedComment(page=page, model=model, path=output_path)
            generated_for_page.append(generated)

            if config.post_mode == "after_each_model":
                print()
                print(
                    f"Posting generated comment for {page} using "
                    f"{model.provider} / {model.model}"
                )
                if not post_generated_comment(
                    repo_root=repo_root,
                    config=config,
                    generated=generated,
                    dry_run=dry_run,
                    post_empty=config.post_empty,
                ):
                    failures += 1
                    if not config.continue_on_error:
                        return 1

            has_more_model_generation = model_index < len(config.models)

            sleep_if_more_work(
                config.delay_seconds,
                dry_run=dry_run,
                has_more_work=has_more_model_generation,
            )

        if config.post_mode == "after_page":
            print()
            print(f"Posting generated comments for page: {page}")

            for generated_index, generated in enumerate(generated_for_page, start=1):
                print()
                print(
                    f"Posting {generated_index}/{len(generated_for_page)}: "
                    f"{generated.path}"
                )

                if not post_generated_comment(
                    repo_root=repo_root,
                    config=config,
                    generated=generated,
                    dry_run=dry_run,
                    post_empty=config.post_empty,
                ):
                    failures += 1
                    if not config.continue_on_error:
                        return 1

                has_more_posting_or_pages = (
                    generated_index < len(generated_for_page)
                    or page_index < len(config.pages)
                )

                sleep_if_more_work(
                    config.delay_seconds,
                    dry_run=dry_run,
                    has_more_work=has_more_posting_or_pages,
                )

    print()
    print("=" * 80)
    print("Batch complete")
    print(f"Failures: {failures}")
    print("=" * 80)

    return 0 if failures == 0 else 1


def main() -> int:
    args = parse_args()

    try:
        repo_root = get_repo_root()
        config_path = Path(args.config)
        if not config_path.is_absolute():
            config_path = repo_root / config_path

        config = load_batch_config(config_path, repo_root)
        config = apply_cli_overrides(config, args)

        return run_batch(config, repo_root=repo_root, dry_run=args.dry_run)

    except BatchReviewError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
