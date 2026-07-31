# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Plaintext / HTML / CSV / Markdown extraction (stdlib)."""

from __future__ import annotations

import re
from typing import Optional

from ..types import ExtractedDocument

_TAG_RE = re.compile(r"<[^>]+>")


def extract_plaintext(
    data: bytes,
    *,
    source: Optional[str] = None,
    format_hint: str = "plaintext",
) -> ExtractedDocument:
    text = data.decode("utf-8", errors="replace")
    fmt = format_hint or "plaintext"
    if fmt in ("html", "htm"):
        text = _TAG_RE.sub(" ", text)
        text = re.sub(r"\s+", " ", text).strip()
        fmt = "html"
    return ExtractedDocument(text=text, format=fmt, source=source)
