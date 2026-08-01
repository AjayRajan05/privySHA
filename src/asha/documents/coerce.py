# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Coerce file paths / bytes into prompt text for drop-in APIs."""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Optional, Union

from .extractors.base import KNOWN_EXTENSIONS, extract_text

PromptInput = Union[str, Path, bytes, BinaryIO]


def _looks_like_document_path(value: str) -> bool:
    path = Path(value)
    if path.suffix.lower() not in KNOWN_EXTENSIONS:
        return False
    try:
        return path.is_file()
    except OSError:
        return False


def coerce_prompt_input(
    prompt: PromptInput,
    *,
    filename: Optional[str] = None,
) -> str:
    """
    Return plain text for ``process`` / ``sanitize`` / ``optimize``.

    - Normal strings that are not existing document paths are returned as-is.
    - Paths / bytes / file objects are extracted via :func:`extract_text`.
    """
    if isinstance(prompt, Path):
        return extract_text(prompt, filename=filename or prompt.name).text

    if isinstance(prompt, (bytes, bytearray)):
        return extract_text(bytes(prompt), filename=filename).text

    if hasattr(prompt, "read") and not isinstance(prompt, (str, Path)):
        return extract_text(prompt, filename=filename).text

    if isinstance(prompt, str):
        if _looks_like_document_path(prompt):
            return extract_text(prompt, filename=filename).text
        return prompt

    raise TypeError(
        f"Unsupported prompt input type: {type(prompt)!r}. "
        "Expected str, Path, bytes, or a binary file object."
    )
