# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");

"""Core compiler primitives (internal - use process/sanitize at top level).

Eager imports are avoided so ``import asha.core.text`` stays lite.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "apply_stage_flags",
    "build_pipeline_config",
    "policy_from_mode",
    "resolve_effective_privacy",
    "sanitize_text",
    "compile_prompt",
    "optimize_tokens",
]


def __getattr__(name: str) -> Any:
    if name in (
        "apply_stage_flags",
        "build_pipeline_config",
        "policy_from_mode",
        "resolve_effective_privacy",
    ):
        from . import policy_resolution as _pr

        return getattr(_pr, name)
    if name in ("sanitize_text", "compile_prompt", "optimize_tokens"):
        from . import engines as _engines

        return getattr(_engines, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
