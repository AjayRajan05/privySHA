# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""
Drop-in utility functions (NEW - CRITICAL FOR ADOPTION)
from .dropin import process, optimize, sanitize

These functions provide the CRITICAL adoption path:
- process() - One-line prompt processing
- optimize() - Token optimization only
- sanitize() - Security only

File paths / bytes are coerced to text (PDF/DOCX/plaintext) before engines run.
"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Optional, Union

import difflib

from ..core.policy_config import PolicyConfig
from ..runtime.processor import PromptProcessor
from ..runtime.resolve import resolve_process_call, resolve_sanitize_policy
from ..types.results import OptimizeResult, ProcessResult, SanitizeResult
from .dropin_helpers import coerce_process_output

# Re-export for backward compatibility
_coerce_process_output = coerce_process_output

PromptInput = Union[str, Path, bytes, BinaryIO]


def generate_text_diff(original: str, modified: str) -> str:
    """Generate a readable diff between original and modified text."""
    if original == modified:
        return "No changes made"

    diff_lines = list(
        difflib.unified_diff(
            original.splitlines(keepends=True),
            modified.splitlines(keepends=True),
            fromfile="original",
            tofile="modified",
            lineterm="",
        )
    )

    if not diff_lines:
        return "No changes made"

    return "\n".join(diff_lines)


def _coerce(prompt: PromptInput, *, filename: Optional[str] = None) -> str:
    from ..documents.coerce import coerce_prompt_input

    return coerce_prompt_input(prompt, filename=filename)


def process(
    prompt: PromptInput,
    mode: str = "balanced",
    *,
    policy: Optional[PolicyConfig] = None,
    token_budget: int = 1200,
    trace: bool = False,
    debug: bool = False,
    max_retries: int = 0,
    timeout_seconds: Optional[float] = None,
    verbose: bool = False,
    log_level: str = "INFO",
    log_output: str = "console",
    log_file: Optional[str] = None,
    include_legacy_detail: bool = False,
    filename: Optional[str] = None,
) -> ProcessResult:
    """
    Process a prompt through ASHA.

    ``prompt`` may be a string, a path to a text document (``.pdf``, ``.docx``,
    ``.txt``, …), or raw document bytes (pass ``filename=`` when using bytes).

    Most callers only need ``mode`` (``strict``, ``balanced``, ``lite``, ``off``).
    Advanced configuration: ``policy=PolicyConfig(...)``.
    """
    text = _coerce(prompt, filename=filename)
    context, runtime_extras = resolve_process_call(
        mode=mode,
        policy=policy,
        token_budget=token_budget,
        trace=trace,
        debug=debug,
        max_retries=max_retries,
        timeout_seconds=timeout_seconds,
        verbose=verbose,
        log_level=log_level,
        log_output=log_output,
        log_file=log_file,
        include_legacy_detail=include_legacy_detail,
    )

    return PromptProcessor().run_with_context(
        text,
        context,
        **runtime_extras,
    )


async def process_async(
    prompt: PromptInput,
    mode: str = "balanced",
    *,
    policy: Optional[PolicyConfig] = None,
    token_budget: int = 1200,
    trace: bool = False,
    debug: bool = False,
    max_retries: int = 0,
    timeout_seconds: Optional[float] = None,
    verbose: bool = False,
    log_level: str = "INFO",
    log_output: str = "console",
    log_file: Optional[str] = None,
    include_legacy_detail: bool = False,
    filename: Optional[str] = None,
) -> ProcessResult:
    """Async process - returns ProcessResult."""
    import asyncio

    return await asyncio.to_thread(
        process,
        prompt,
        mode=mode,
        policy=policy,
        token_budget=token_budget,
        trace=trace,
        debug=debug,
        max_retries=max_retries,
        timeout_seconds=timeout_seconds,
        verbose=verbose,
        log_level=log_level,
        log_output=log_output,
        log_file=log_file,
        include_legacy_detail=include_legacy_detail,
        filename=filename,
    )


async def optimize_async(
    prompt: PromptInput,
    token_budget: int = 1200,
    trust_input: bool = False,
    *,
    filename: Optional[str] = None,
) -> OptimizeResult:
    """Async tokens-only optimization."""
    import asyncio

    return await asyncio.to_thread(
        optimize,
        prompt,
        token_budget=token_budget,
        trust_input=trust_input,
        filename=filename,
    )


async def sanitize_async(
    prompt: PromptInput,
    *,
    mode: str = "balanced",
    policy: Optional[PolicyConfig] = None,
    max_retries: int = 0,
    timeout_seconds: Optional[float] = None,
    filename: Optional[str] = None,
) -> SanitizeResult:
    """Async sanitize - observable failure on detector errors."""
    import asyncio

    return await asyncio.to_thread(
        sanitize,
        prompt,
        mode=mode,
        policy=policy,
        max_retries=max_retries,
        timeout_seconds=timeout_seconds,
        filename=filename,
    )


def optimize(
    prompt: PromptInput,
    token_budget: int = 1200,
    trust_input: bool = False,
    *,
    filename: Optional[str] = None,
) -> OptimizeResult:
    """Token optimization only via MSDPC - no security or compile stages."""
    from ..core.engines import optimize_tokens

    text = _coerce(prompt, filename=filename)
    if trust_input:
        from ..types.results import MetricsInfo
        return OptimizeResult(
            output=text,
            original=text,
            degraded=False,
            degraded_reason=None,
            metrics=MetricsInfo(0, 0.0, 0.0),
        )
    return optimize_tokens(text, token_budget=token_budget)


def sanitize(
    prompt: PromptInput,
    *,
    mode: str = "balanced",
    policy: Optional[PolicyConfig] = None,
    max_retries: int = 0,
    timeout_seconds: Optional[float] = None,
    filename: Optional[str] = None,
) -> SanitizeResult:
    """
    Sanitize a prompt for security only (PII masking, threat detection).

    ``prompt`` may be a string, document path, or bytes (see ``process``).

    Use ``mode="strict"`` to block on failure; ``mode="balanced"`` for degraded fallback.
    Advanced: ``policy=PolicyConfig(reversible=True)``.
    """
    from ..core.engines import sanitize_text

    text = _coerce(prompt, filename=filename)
    safety, reversible, pii_mode = resolve_sanitize_policy(mode, policy)
    return sanitize_text(
        text,
        reversible=reversible,
        safety_mode=safety,
        mode=mode,
        max_retries=max_retries,
        timeout_seconds=timeout_seconds,
        pii_mode=pii_mode,
    )
