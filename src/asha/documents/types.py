# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Types for extracted documents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ExtractedDocument:
    """Plain text extracted from a supported document format."""

    text: str
    format: str
    source: Optional[str] = None
    page_count: Optional[int] = None
