"""LlamaIndex integration (skips if asha[llamaindex] not installed)."""

from __future__ import annotations

from typing import Any

import pytest

pytest.importorskip("llama_index")

from asha.runtime.anchor.adapters.llamaindex import anchor_llamaindex


class _StubQueryEngine:
    __module__ = "llama_index.core.query_engine"

    def __init__(self) -> None:
        self.tools: list[Any] = []

    def query(self, *args: Any, **kwargs: Any) -> str:
        return f"answer:{args[0] if args else ''}"


def test_llama_index_importable() -> None:
    import llama_index.core

    assert llama_index.core is not None


def test_anchor_llamaindex_wraps_when_package_present() -> None:
    wrapped = anchor_llamaindex(_StubQueryEngine(), interactive=False)
    out = wrapped.query("Summarize the local index.")
    assert out is not None
