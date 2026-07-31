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

"""Unicode canonicalization for lite-tier detectors (stdlib-only).

Pipeline (in order):
1. NFKC normalize
2. Strip Default_Ignorable / zero-width / invisible format chars
3. Fold common confusables (Cyrillic/Greek/fullwidth) to ASCII
4. Optionally produce a leetspeak-folded sibling view
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Iterable

from .confusables_table import CONFUSABLES, LEETSPEAK

# Explicit high-signal invisibles (subset of Default_Ignorable_Code_Point).
# Combined with category-based detection below.
_EXPLICIT_INVISIBLES = frozenset(
    {
        "\u00ad",  # soft hyphen
        "\u034f",  # combining grapheme joiner
        "\u061c",  # Arabic letter mark
        "\u115f",  # Hangul choseong filler
        "\u1160",  # Hangul jungseong filler
        "\u17b4",  # Khmer vowel inherent aq
        "\u17b5",  # Khmer vowel inherent aa
        "\u180b",  # Mongolian free variation selector one
        "\u180c",
        "\u180d",
        "\u180e",  # Mongolian vowel separator
        "\u200b",  # zero width space
        "\u200c",  # zero width non-joiner
        "\u200d",  # zero width joiner
        "\u200e",  # LTR mark
        "\u200f",  # RTL mark
        "\u202a",  # LRE
        "\u202b",  # RLE
        "\u202c",  # PDF
        "\u202d",  # LRO
        "\u202e",  # RLO
        "\u2060",  # word joiner
        "\u2061",  # function application
        "\u2062",  # invisible times
        "\u2063",  # invisible separator
        "\u2064",  # invisible plus
        "\u2066",  # LRI
        "\u2067",  # RLI
        "\u2068",  # FSI
        "\u2069",  # PDI
        "\u206a",  # inhibit symmetric swapping
        "\u206b",
        "\u206c",
        "\u206d",
        "\u206e",
        "\u206f",
        "\ufeff",  # BOM / ZWNBSP
        "\ufff9",  # interlinear annotation anchor
        "\ufffa",
        "\ufffb",
    }
)

# Unicode categories treated as default-ignorable for our purposes.
_IGNORABLE_CATEGORIES = frozenset({"Cf", "Cc", "Mn"})


def _is_ignorable(ch: str) -> bool:
    if ch in _EXPLICIT_INVISIBLES:
        return True
    cat = unicodedata.category(ch)
    if cat in _IGNORABLE_CATEGORIES:
        # Keep ordinary combining accents that affect meaning (Mn on letters
        # like é) only when they are not variation selectors / fillers.
        # Soft rule: strip Cf/Cc always; strip Mn only if name suggests
        # variation selector / invisible / filler.
        if cat == "Mn":
            name = unicodedata.name(ch, "")
            return any(
                token in name
                for token in (
                    "VARIATION SELECTOR",
                    "ZERO WIDTH",
                    "INVISIBLE",
                    "FILLER",
                    "TAG ",
                )
            )
        return True
    # Variation selectors outside Cf
    cp = ord(ch)
    if 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF:
        return True
    return False


def _strip_ignorables(text: str) -> str:
    return "".join(ch for ch in text if not _is_ignorable(ch))


def _fold_confusables(text: str) -> str:
    return "".join(CONFUSABLES.get(ch, ch) for ch in text)


def _fold_leetspeak(text: str) -> str:
    lower = text.lower()
    return "".join(LEETSPEAK.get(ch, ch) for ch in lower)


@dataclass(frozen=True)
class CanonicalViews:
    """Two views of the same input for dual-path matching."""

    canonical: str
    leetspeak: str

    def all_views(self) -> tuple[str, str]:
        return self.canonical, self.leetspeak


def canonicalize(text: str) -> str:
    """NFKC → strip ignorables → confusable fold.

    This is the primary form used before regex / Aho-Corasick / hashed features.
    """
    if not text:
        return ""
    nfkc = unicodedata.normalize("NFKC", text)
    stripped = _strip_ignorables(nfkc)
    return _fold_confusables(stripped)


def canonicalize_views(text: str) -> CanonicalViews:
    """Return canonical + leetspeak-folded views (leetspeak is lossy)."""
    canon = canonicalize(text)
    return CanonicalViews(canonical=canon, leetspeak=_fold_leetspeak(canon))


def expand_for_matching(text: str) -> Iterable[str]:
    """Yield unique views suitable for multi-view pattern scans."""
    views = canonicalize_views(text)
    seen: set[str] = set()
    for v in views.all_views():
        if v and v not in seen:
            seen.add(v)
            yield v
