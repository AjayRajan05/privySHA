"""Hybrid PII mode tests."""

from asha import process
from asha.core.policy_config import PolicyConfig
from asha.types.results import ProcessResult

from conftest import output_of


def test_hybrid_pii_mode_runs_or_falls_back():
    """Hybrid mode masks PII via the layered pipeline."""
    email = "alice.chen@acme-corp.com"
    prompt = f"Contact {email}"
    result = process(prompt, policy=PolicyConfig(pii_mode="hybrid"))
    assert isinstance(result, ProcessResult)
    out = output_of(result)
    assert email not in out
    assert (
        "email" in out.lower()
        or "Contact" in out
        or (result.security is not None and bool(result.security.pii_detected))
    )
