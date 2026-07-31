# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""ASHA public exceptions and warnings."""

from __future__ import annotations

import warnings


class ASHAError(Exception):
    """Base exception for ASHA errors."""


class ASHAWrapError(ASHAError):
    """Raised when wrap_llm() cannot apply privacy protection."""


class ASHAProcessingError(ASHAError):
    """Raised when prompt processing fails in fail-closed mode."""


class ASHAAnchorBlocked(ASHAError):
    """Raised when ANCHOR blocks an agent action or tool call."""


class ASHAExperimentalWarning(UserWarning):
    """API is experimental and may change without a deprecation cycle."""


def warn_experimental(feature: str, *, stacklevel: int = 3) -> None:
    """Emit a one-line experimental warning for preview APIs."""
    warnings.warn(
        f"{feature} is experimental in ASHA 0.4.2 and may change without "
        "a deprecation cycle. Prefer process/sanitize/optimize/wrap_llm for "
        "stable drop-in usage. See docs/experimental-features.md.",
        ASHAExperimentalWarning,
        stacklevel=stacklevel,
    )