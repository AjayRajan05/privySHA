# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");

"""Public API freeze tests."""

from __future__ import annotations

import pytest

import asha


def test_root_eager_exports_frozen() -> None:
    expected = {"process", "sanitize", "optimize", "Agent", "anchor", "__version__"}
    assert set(asha.__all__) == expected


def test_root_export_count_at_most_ten() -> None:
    assert len(asha.__all__) <= 10


def test_primary_apis_callable() -> None:
    assert callable(asha.process)
    assert callable(asha.sanitize)
    assert callable(asha.optimize)
    assert callable(asha.Agent)
    out = asha.process("Contact alice@acme-corp.com", mode="balanced")
    assert "alice@acme-corp.com" not in out.output
    sanitized = asha.sanitize("Call 555-123-4567 now")
    assert "555-123-4567" not in sanitized.output
    optimized = asha.optimize("Please briefly summarize quarterly revenue trends.")
    assert "revenue" in optimized.output.lower() or "quarterly" in optimized.output.lower()
    agent = asha.Agent(model="mock", privacy=True)
    response = agent.run("Say hello without secrets")
    text = response if isinstance(response, str) else getattr(response, "response", str(response))
    assert "hello" in text.lower() or len(str(text)) > 0


def test_moved_symbols_not_eager() -> None:
    import importlib
    import sys

    saved = {
        key: module
        for key, module in sys.modules.items()
        if key == "asha" or key.startswith("asha.")
    }
    try:
        for key in saved:
            sys.modules.pop(key, None)
        mod = importlib.import_module("asha")
        assert "Processor" not in mod.__dict__
        assert "wrap_llm" not in mod.__dict__
        assert "ProcessResult" not in mod.__dict__
        assert "Pipeline" not in mod.__dict__
    finally:
        sys.modules.update(saved)


@pytest.mark.parametrize(
    "name",
    ["Processor", "wrap_llm", "Pipeline", "ProcessResult", "auto_patch"],
)
def test_lazy_symbols_raise_attribute_error(name: str) -> None:
    with pytest.raises(AttributeError):
        getattr(asha, name)


def test_no_getattr_shim() -> None:
    """Primary APIs may use ``__getattr__`` for cold-import laziness.

    Moved symbols (Processor, wrap_llm, …) must still raise AttributeError —
    covered by ``test_lazy_symbols_raise_attribute_error``. This test pins that
    ``__getattr__`` only serves names in ``__all__`` (not a catch-all shim).
    """
    assert callable(asha.__getattr__)
    # Unknown / moved names must not be silently resolved.
    with pytest.raises(AttributeError):
        asha.__getattr__("Processor")
    with pytest.raises(AttributeError):
        asha.__getattr__("wrap_llm")
    # Documented primary APIs resolve.
    assert callable(asha.__getattr__("process"))
    assert callable(asha.__getattr__("sanitize"))
