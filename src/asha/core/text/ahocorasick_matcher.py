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

"""Aho-Corasick multi-pattern matcher (stdlib fallback + optional accelerator).

Fast path: ``pyahocorasick`` when installed.
Fallback: pure-Python trie + BFS failure links (standard Aho-Corasick).
Both paths return identical ``Match`` results for the same pattern set.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

PatternSpec = Union[
    Tuple[str, str],
    Tuple[str, str, float],
]


@dataclass(frozen=True)
class Match:
    """One pattern hit in a scanned text."""

    start: int
    end: int
    pattern: str
    label: str
    weight: float


class _TrieNode:
    __slots__ = ("children", "fail", "outputs")

    def __init__(self) -> None:
        self.children: Dict[str, _TrieNode] = {}
        self.fail: Optional[_TrieNode] = None
        self.outputs: List[Tuple[str, str, float]] = []


class _PurePythonAutomaton:
    """Classic Aho-Corasick: trie + failure links + output links."""

    def __init__(self) -> None:
        self.root = _TrieNode()
        self._built = False

    def add(self, pattern: str, label: str, weight: float) -> None:
        if not pattern:
            return
        node = self.root
        for ch in pattern:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.outputs.append((pattern, label, weight))
        self._built = False

    def build(self) -> None:
        root = self.root
        root.fail = root
        q: deque[_TrieNode] = deque()
        for child in root.children.values():
            child.fail = root
            q.append(child)

        while q:
            current = q.popleft()
            for ch, nxt in current.children.items():
                q.append(nxt)
                fail = current.fail
                assert fail is not None
                while fail is not root and ch not in fail.children:
                    fail = fail.fail or root
                nxt.fail = fail.children.get(ch, root) if fail is not None else root
                if nxt.fail is nxt:
                    nxt.fail = root
                # Inherit outputs along failure link
                if nxt.fail.outputs:
                    nxt.outputs = list(nxt.outputs) + list(nxt.fail.outputs)
        self._built = True

    def scan(self, text: str) -> List[Match]:
        if not self._built:
            self.build()
        matches: List[Match] = []
        node = self.root
        for i, ch in enumerate(text):
            while node is not self.root and ch not in node.children:
                node = node.fail or self.root
            node = node.children.get(ch, self.root)
            if node.outputs:
                for pattern, label, weight in node.outputs:
                    end = i + 1
                    start = end - len(pattern)
                    matches.append(
                        Match(
                            start=start,
                            end=end,
                            pattern=pattern,
                            label=label,
                            weight=weight,
                        )
                    )
        return matches


class _PyAhoCorasickAutomaton:
    """Thin wrapper around pyahocorasick with the same Match API."""

    def __init__(self) -> None:
        import ahocorasick  # type: ignore

        self._A = ahocorasick.Automaton()
        self._meta: Dict[str, Tuple[str, float]] = {}
        self._built = False

    def add(self, pattern: str, label: str, weight: float) -> None:
        if not pattern:
            return
        # Store pattern as value; label/weight looked up from meta.
        key = pattern
        self._A.add_word(key, key)
        self._meta[key] = (label, weight)
        self._built = False

    def build(self) -> None:
        self._A.make_automaton()
        self._built = True

    def scan(self, text: str) -> List[Match]:
        if not self._built:
            self.build()
        matches: List[Match] = []
        for end_idx, pattern in self._A.iter(text):
            label, weight = self._meta[pattern]
            end = end_idx + 1
            start = end - len(pattern)
            matches.append(
                Match(
                    start=start,
                    end=end,
                    pattern=pattern,
                    label=label,
                    weight=weight,
                )
            )
        return matches


def _normalize_specs(
    patterns: Sequence[PatternSpec],
) -> List[Tuple[str, str, float]]:
    out: List[Tuple[str, str, float]] = []
    for item in patterns:
        if len(item) == 2:
            pattern, label = item  # type: ignore[misc]
            weight = 1.0
        else:
            pattern, label, weight = item  # type: ignore[misc]
        out.append((str(pattern), str(label), float(weight)))
    return out


class PatternMatcher:
    """Multi-pattern scanner with identical results on both backends."""

    def __init__(
        self,
        patterns: Optional[Sequence[PatternSpec]] = None,
        *,
        case_insensitive: bool = True,
        prefer_native: bool = True,
    ) -> None:
        self.case_insensitive = case_insensitive
        self._backend_name = "pure"
        self._auto: Union[_PurePythonAutomaton, _PyAhoCorasickAutomaton]
        if prefer_native:
            try:
                self._auto = _PyAhoCorasickAutomaton()
                self._backend_name = "pyahocorasick"
            except ImportError:
                self._auto = _PurePythonAutomaton()
        else:
            self._auto = _PurePythonAutomaton()

        if patterns:
            for pattern, label, weight in _normalize_specs(patterns):
                self.add(pattern, label, weight)
            self.build()

    @property
    def backend(self) -> str:
        return self._backend_name

    def add(self, pattern: str, label: str, weight: float = 1.0) -> None:
        p = pattern.lower() if self.case_insensitive else pattern
        self._auto.add(p, label, weight)

    def build(self) -> None:
        self._auto.build()

    def scan(self, text: str) -> List[Match]:
        hay = text.lower() if self.case_insensitive else text
        return self._auto.scan(hay)

    @classmethod
    def from_patterns(
        cls,
        patterns: Sequence[PatternSpec],
        *,
        case_insensitive: bool = True,
        prefer_native: bool = True,
    ) -> "PatternMatcher":
        return cls(
            patterns,
            case_insensitive=case_insensitive,
            prefer_native=prefer_native,
        )
