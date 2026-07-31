"""Tests for optimize() API - tokens-only in v0.4."""

from asha import optimize
from asha.types.results import OptimizeResult


def test_optimize_returns_optimize_result():
    prompt = "Summarize quarterly sales trends."
    result = optimize(prompt)
    assert result.output == prompt
    assert "summarize" in result.output.lower()
    assert "sales" in result.output.lower()


def test_optimize_trust_input_bypasses_compression():
    prompt = "Contact john@company.com unchanged"
    result = optimize(prompt, trust_input=True)
    assert isinstance(result, OptimizeResult)
    assert result.output == prompt


def test_optimize_tokens_only_may_keep_pii():
    """optimize() does not run security - email may remain."""
    prompt = "Contact secret@company.com for help"
    result = optimize(prompt)
    assert "secret@company.com" in result.output
    assert "help" in result.output


def test_optimize_token_budget():
    long_prompt = "word " * 500
    result = optimize(long_prompt, token_budget=50)
    assert result.metrics is not None
    assert result.metrics.tokens_saved > 0
    assert result.metrics.token_reduction_pct > 0
    assert "word" in result.output


def test_optimize_empty_prompt():
    result = optimize("")
    assert isinstance(result, OptimizeResult)
    assert result.output == ""
