# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Lightweight locale detection for PII recognizer selection.

Non-generative. Uses ``langdetect`` when available; otherwise heuristic
cues (scripts, +91, Indian ID keywords). Uncertain → default locale set.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LocaleGuess:
    locale: str  # e.g. "en_IN", "en_US", "ta", "hi", "unknown"
    confidence: float
    source: str


_IN_KEYWORDS = re.compile(
    r"(?i)\b(aadhaar|aadhar|uidai|pan\b|gstin|gst\b|rupee|₹|chennai|mumbai|"
    r"bengaluru|bangalore|delhi|hyderabad|kolkata|tamil|hindi)\b"
)
_PLUS_91 = re.compile(r"\+91[\s-]?\d")
_DEVANAGARI = re.compile(r"[\u0900-\u097F]")
_TAMIL = re.compile(r"[\u0B80-\u0BFF]")


def detect_locale(text: str) -> LocaleGuess:
    """Guess a locale for selecting PII recognizer sets.

    When detection is uncertain, returns ``en_IN``-aware default so Indian
    formats are not silently missed for this user base.
    """
    if not text or not text.strip():
        return LocaleGuess(locale="en_IN", confidence=0.3, source="empty_default")

    # Script cues (high confidence).
    if _TAMIL.search(text):
        return LocaleGuess(locale="ta_IN", confidence=0.85, source="tamil_script")
    if _DEVANAGARI.search(text):
        return LocaleGuess(locale="hi_IN", confidence=0.85, source="devanagari")

    in_score = 0.0
    if _IN_KEYWORDS.search(text):
        in_score += 0.4
    if _PLUS_91.search(text):
        in_score += 0.35

    # Optional langdetect.
    lang: Optional[str] = None
    try:
        from langdetect import detect_langs

        guesses = detect_langs(text[:2000])
        if guesses:
            top = guesses[0]
            lang = top.lang
            if lang in ("ta", "hi", "te", "ml", "kn", "mr", "bn"):
                return LocaleGuess(
                    locale=f"{lang}_IN",
                    confidence=min(0.95, float(top.prob)),
                    source="langdetect",
                )
            if lang == "en" and in_score >= 0.35:
                return LocaleGuess(
                    locale="en_IN",
                    confidence=min(0.9, 0.5 + in_score),
                    source="langdetect+in_cues",
                )
            if lang == "en":
                return LocaleGuess(
                    locale="en_US" if in_score < 0.2 else "en_IN",
                    confidence=float(top.prob) * 0.8,
                    source="langdetect",
                )
    except Exception:
        pass

    if in_score >= 0.35:
        return LocaleGuess(
            locale="en_IN", confidence=min(0.85, 0.4 + in_score), source="in_cues"
        )

    # Uncertain → default recognizer set includes Indian formats (fail-open for
    # detection coverage, not for security decisions).
    return LocaleGuess(locale="en_IN", confidence=0.35, source="uncertain_default")
