#!/usr/bin/env python3
"""Translate registry reasoning policy into provider-supported request fields."""

from __future__ import annotations

from typing import Any

from provider_model_registry import ProviderModelSlot, RegistryValidationError


def _require_provider(slot: ProviderModelSlot, provider: str) -> None:
    if slot.provider != provider:
        raise RegistryValidationError(f"Reasoning request builder for {provider} received registry slot {slot.spec}.")


def groq_request_kwargs(slot: ProviderModelSlot) -> dict[str, Any]:
    """Return only Groq chat-completion fields supported by the configured model."""
    _require_provider(slot, "groq")
    reasoning = slot.request_config.get("reasoning")
    if slot.model in {"openai/gpt-oss-120b", "openai/gpt-oss-20b"} and reasoning == "low":
        effort = "low"
    elif slot.model == "qwen/qwen3.6-27b" and reasoning == "none":
        effort = "none"
    else:
        raise RegistryValidationError(f"Unsupported Groq reasoning configuration for {slot.spec}.")
    return {"reasoning_effort": effort, "include_reasoning": False}


def sambanova_request_kwargs(slot: ProviderModelSlot) -> dict[str, Any]:
    """Return documented SambaNova chat-completion reasoning fields, when supported."""
    _require_provider(slot, "sambanova")
    if slot.model == "gpt-oss-120b" and slot.request_config.get("reasoning") == "low-where-supported":
        return {"reasoning_effort": "low"}
    return {}


def gemini_thinking_kwargs(slot: ProviderModelSlot) -> dict[str, Any]:
    """Return arguments for ``google.genai.types.ThinkingConfig``."""
    _require_provider(slot, "gemini")
    request_config = slot.request_config
    if "thinking_level" in request_config:
        return {"thinking_level": request_config["thinking_level"], "include_thoughts": False}
    if "thinking_budget" in request_config:
        return {"thinking_budget": request_config["thinking_budget"], "include_thoughts": False}
    raise RegistryValidationError(f"Gemini slot {slot.spec} has no supported thinking configuration.")


def openrouter_extra_body(slot: ProviderModelSlot) -> dict[str, Any]:
    """Return OpenRouter routing and normalized reasoning controls."""
    _require_provider(slot, "openrouter")
    reasoning = slot.request_config.get("reasoning")
    effort = {
        "lowest-supported": "minimal",
        "low": "low",
        "none": "none",
        "none-unless-required": "none",
    }.get(reasoning)
    if effort is None:
        raise RegistryValidationError(f"Unsupported OpenRouter reasoning configuration for {slot.spec}.")
    return {
        "provider": {"allow_fallbacks": False},
        "reasoning": {"effort": effort, "exclude": True},
    }
