# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Text-document extraction for PII masking of file inputs (no OCR)."""

from __future__ import annotations

from .attachments import prepare_llm_request_kwargs
from .coerce import coerce_prompt_input
from .extractors import extract_text

__all__ = [
    "coerce_prompt_input",
    "extract_text",
    "prepare_llm_request_kwargs",
]
