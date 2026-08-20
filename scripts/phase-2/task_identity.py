#!/usr/bin/env python3
"""Build deterministic content-addressed identities for Phase 2 tasks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from provider_model_registry import ProviderModelSlot

PHASE = "phase-2"
SEGMENTATION_PROFILE = "full-page-v1"
VALIDATOR_VERSION = "check-signal-schema-v1"

LANGUAGE_STYLE_EXCLUDED_SECTIONS = {
    "references",
    "direct citations",
    "consulted sources",
    "generation and review log",
}

MARKDOWN_HEADING_PATTERN = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$")
FENCED_BLOCK_PATTERN = re.compile(r"^\s*(```|~~~)")


class TaskIdentityError(ValueError):
    """Raised when a deterministic task identity cannot be constructed."""


def build_review_input(
    *,
    checker_prompt: str,
    agent: str,
    provider: str,
    model: str,
    prompt_id: str,
    review_date: str,
    page_path: str,
    commit_sha: str,
    max_completion_tokens: int | str,
    page_content: str,
    input_scope_note: str,
) -> str:
    """Render the exact prompt sent to a check-agent provider."""
    return f"""# Stable check-agent contract

{checker_prompt}

---

# Run input

agent: {agent}
provider: {provider}
model: {model}
prompt: {prompt_id}
date: {review_date}
page: {page_path}
commit: {commit_sha}
output-token-cap: {max_completion_tokens}
input-scope: {input_scope_note}

---

# Agent-scoped canonical page Markdown

BEGIN_CANONICAL_STEREOTYPE_PAGE_MARKDOWN
{page_content}
END_CANONICAL_STEREOTYPE_PAGE_MARKDOWN
"""


def build_effective_prompt_content(
    *,
    checker_prompt: str,
    agent: str,
    prompt_id: str,
    input_scope_note: str,
) -> str:
    """Render stable effective prompt content with mutable run values excluded."""
    return f"""# Stable check-agent contract

{checker_prompt}

---

# Stable run-input schema

agent: {agent}
prompt: {prompt_id}
input-scope: {input_scope_note}
mutable-fields: provider, model, date, page, commit, output-token-cap, agent-scoped-page-content
"""


def normalize_utf8_text(text: str) -> str:
    """Normalize line endings without changing Markdown content semantics."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sha256_text(text: str) -> str:
    return hashlib.sha256(normalize_utf8_text(text).encode("utf-8")).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_canonical_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def normalize_markdown_section_title(section: str) -> str:
    normalized = section.strip()
    while normalized.startswith("#"):
        normalized = normalized[1:].strip()
    normalized = re.sub(r"\s+#*$", "", normalized).strip()
    return re.sub(r"\s+", " ", normalized).lower()


def remove_markdown_sections(text: str, excluded_sections: set[str]) -> str:
    kept_lines: list[str] = []
    skip_until_heading_level: int | None = None
    in_fenced_block = False
    for line in normalize_utf8_text(text).splitlines():
        if FENCED_BLOCK_PATTERN.match(line):
            if skip_until_heading_level is None:
                kept_lines.append(line)
            in_fenced_block = not in_fenced_block
            continue
        heading_match = None if in_fenced_block else MARKDOWN_HEADING_PATTERN.match(line)
        if heading_match is not None:
            heading_level = len(heading_match.group("hashes"))
            heading_title = normalize_markdown_section_title(heading_match.group("title"))
            if skip_until_heading_level is not None and heading_level <= skip_until_heading_level:
                skip_until_heading_level = None
            if skip_until_heading_level is None and heading_title in excluded_sections:
                skip_until_heading_level = heading_level
                continue
        if skip_until_heading_level is None:
            kept_lines.append(line)
    scoped_text = "\n".join(kept_lines).strip()
    return scoped_text + "\n" if scoped_text else ""


def scope_page_content_for_agent(*, agent: str, page_content: str) -> tuple[str, str]:
    normalized_content = normalize_utf8_text(page_content)
    if agent != "language-style-checker":
        return normalized_content, "full canonical stereotype page"
    scoped_content = remove_markdown_sections(normalized_content, LANGUAGE_STYLE_EXCLUDED_SECTIONS)
    if not scoped_content.strip():
        raise TaskIdentityError("Language-style input scoping removed all page content.")
    return (
        scoped_content,
        "reader-facing page content only; excluded References, Direct Citations, Consulted Sources, "
        "and Generation and Review Log sections",
    )


def effective_request_configuration(
    slot: ProviderModelSlot,
    *,
    max_completion_tokens: int | None = None,
) -> dict[str, Any]:
    request_config = dict(slot.request_config)
    effective_max_tokens = slot.max_completion_tokens if max_completion_tokens is None else max_completion_tokens
    request_config["max_completion_tokens"] = effective_max_tokens
    return {
        "request_config_version": slot.request_config_version,
        "reasoning_policy": slot.reasoning_policy,
        "output_policy": slot.output_policy,
        "max_completion_tokens": effective_max_tokens,
        "request_config": request_config,
    }


def build_task_identity(
    *,
    page: str,
    agent: str,
    provider: str,
    model: str,
    page_content: str,
    prompt_id: str,
    prompt_content: str,
    slot: ProviderModelSlot,
    max_completion_tokens: int | None = None,
) -> dict[str, str]:
    normalized_page = Path(page).as_posix().lstrip("./")
    if slot.provider != provider or slot.model != model:
        raise TaskIdentityError(
            f"Registry slot {slot.spec} does not match requested provider/model {provider}:{model}."
        )
    if agent not in slot.agents:
        raise TaskIdentityError(f"Agent {agent!r} is not configured for registry slot {slot.spec}.")
    scoped_content, input_scope_note = scope_page_content_for_agent(agent=agent, page_content=page_content)
    request_config = effective_request_configuration(slot, max_completion_tokens=max_completion_tokens)
    effective_prompt = build_effective_prompt_content(
        checker_prompt=prompt_content,
        agent=agent,
        prompt_id=prompt_id,
        input_scope_note=input_scope_note,
    )
    return {
        "phase": PHASE,
        "page": normalized_page,
        "agent": agent,
        "provider": provider,
        "model": model,
        "content_sha256": sha256_text(scoped_content),
        "prompt_id": prompt_id,
        "prompt_sha256": sha256_text(effective_prompt),
        "validator_version": VALIDATOR_VERSION,
        "request_config_sha256": sha256_canonical_json(request_config),
        "segmentation_profile": SEGMENTATION_PROFILE,
    }


def task_id_for(identity: dict[str, str]) -> str:
    return sha256_canonical_json(identity)
