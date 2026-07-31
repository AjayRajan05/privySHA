"""Tests for v0.4 typed results and API semantics."""

import asyncio

import pytest

from asha import process, sanitize, optimize
from asha.integrations import wrap_llm
from asha.types import (
    AgentResult,
    OptimizeResult,
    ProcessResult,
    SanitizeResult,
)
from asha.exceptions import ASHAWrapError
from asha.utils.dropin import optimize_async, process_async, sanitize_async


def test_process_returns_process_result():
    result = process("Contact john@example.com for help")
    assert isinstance(result, ProcessResult)
    assert "john@example.com" not in result.output
    assert str(result) == result.output


def test_sanitize_returns_sanitize_result():
    result = sanitize("Contact john@example.com for analysis")
    assert isinstance(result, SanitizeResult)
    assert "john@example.com" not in result.output


def test_optimize_is_tokens_only():
    prompt = "Hey bro can you please analyze this dataset for anomalies?"
    result = optimize(prompt)
    assert result.output == prompt
    assert "analyze" in result.output.lower()
    assert "dataset" in result.output.lower()
    assert "anomalies" in result.output.lower()


def test_optimize_skips_security():
    prompt = "Contact john@example.com for help"
    result = optimize(prompt)
    assert isinstance(result, OptimizeResult)
    assert "john@example.com" in result.output


def test_process_mode_off_skips_pii():
    prompt = "Contact john@example.com for help"
    result = process(prompt, mode="off")
    assert "john@example.com" in result.output


def test_sanitize_observable_failure(monkeypatch):
    def boom(*_a, **_k):
        raise RuntimeError("detector down")

    monkeypatch.setattr(
        "asha.core.engines.run_security_only",
        boom,
    )
    result = sanitize("test@example.com")
    assert isinstance(result, SanitizeResult)
    assert result.degraded is True
    assert result.safe is False


def test_process_balanced_failure_no_raw_pii(monkeypatch):
    def boom(*_a, **_k):
        raise RuntimeError("security down")

    monkeypatch.setattr(
        "asha.core.security.service.run_security",
        boom,
    )
    result = process("Email john@example.com now", mode="balanced")
    assert isinstance(result, ProcessResult)
    assert "john@example.com" not in result.output


def test_process_async_returns_process_result():
    result = asyncio.run(
        process_async("Contact john@example.com for help", mode="balanced")
    )
    assert isinstance(result, ProcessResult)
    assert "john@example.com" not in result.output


def test_sanitize_async_returns_sanitize_result():
    result = asyncio.run(sanitize_async("Contact alice@acme.com for help"))
    assert isinstance(result, SanitizeResult)
    assert "alice@acme.com" not in result.output


def test_optimize_async_returns_optimize_result():
    prompt = "hello world please summarize"
    result = asyncio.run(optimize_async(prompt))
    assert result.output == prompt
    assert "summarize" in result.output.lower()
    assert "hello" in result.output.lower()


def test_agent_trace_returns_agent_result():
    from asha import Agent

    agent = Agent(model="mock", privacy=True)
    prompt = "Contact john@example.com for help"
    out = agent.run(prompt, trace=True)
    assert out.original == prompt
    assert "john@example.com" not in out.output
    assert "john@example.com" not in out.response
    assert "Mock" in out.response


def test_wrap_llm_invalid_raises():
    class BadClient:
        pass

    with pytest.raises(ValueError):
        wrap_llm(BadClient())
