# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""PDF text-layer extraction via pypdf (no OCR)."""

from __future__ import annotations

import io
from typing import Optional

from ..types import ExtractedDocument


def extract_pdf(data: bytes, *, source: Optional[str] = None) -> ExtractedDocument:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    parts: list[str] = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            parts.append("")
    text = "\n".join(parts).strip()
    return ExtractedDocument(
        text=text,
        format="pdf",
        source=source,
        page_count=len(reader.pages),
    )
