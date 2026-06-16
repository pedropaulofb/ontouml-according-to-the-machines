#!/usr/bin/env python3
"""Compile active repository Python scripts without importing them.

This pre-commit helper intentionally skips scripts/local/ because that directory
is ignored and may contain machine-local experiments or credentials-dependent
helpers outside the canonical repository infrastructure.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SKIPPED_PARTS = {"local"}


@dataclass(frozen=True)
class CompileFailure:
    """One Python compilation failure."""

    path: Path
    error: str


def find_repo_root() -> Path:
    """Return the repository root."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("Could not determine the repository root with git.") from exc

    repo_root = Path(result.stdout.strip()).resolve()
    if not repo_root.is_dir():
        raise RuntimeError(f"Resolved repository root is not a directory: {repo_root}")
    return repo_root


def should_skip(path: Path, scripts_root: Path) -> bool:
    """Return whether a Python file should be skipped."""
    try:
        relative = path.relative_to(scripts_root)
    except ValueError:
        return True

    return any(part in SKIPPED_PARTS for part in relative.parts)


def discover_python_files(repo_root: Path) -> list[Path]:
    """Discover active Python files under scripts/."""
    scripts_root = repo_root / "scripts"
    if not scripts_root.is_dir():
        return []

    return sorted(path for path in scripts_root.rglob("*.py") if path.is_file() and not should_skip(path, scripts_root))


def compile_file(path: Path, repo_root: Path) -> CompileFailure | None:
    """Compile one Python file and return a failure object when compilation fails."""
    relative_path = path.relative_to(repo_root)

    try:
        source = path.read_text(encoding="utf-8")
        compile(source, str(relative_path), "exec")
    except Exception as exc:  # noqa: BLE001 - this is a diagnostic wrapper.
        return CompileFailure(path=relative_path, error=f"{type(exc).__name__}: {exc}")

    return None


def main() -> int:
    """Compile active Python scripts."""
    try:
        repo_root = find_repo_root()
        python_files = discover_python_files(repo_root)
        failures = [failure for path in python_files if (failure := compile_file(path, repo_root)) is not None]

        print(f"Python files checked: {len(python_files)}")

        if failures:
            print("Python compilation failures:", file=sys.stderr)
            for failure in failures:
                print(f"- {failure.path}: {failure.error}", file=sys.stderr)
            return 1

        return 0

    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
