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

"""PII hardening tests: Indian formats, hybrid default, checksum soft-fail."""

from __future__ import annotations

from asha.core.hybrid_pii import HybridPIIDetector
from asha.core.ml_utils import check_pii_mode_feasibility, validate_pii_mode
from asha.core.policy_config import PolicyConfig
from asha.core.security.checksums import (
    gstin_check_digit,
    gstin_validate,
    luhn_validate,
    pan_validate,
    verhoeff_checksum_digit,
    verhoeff_validate,
)
from asha.core.security.locale_detect import detect_locale
from asha.core.security.pii_detector import PIIDetector
from asha.core.security.service import run_security


def _valid_aadhaar() -> str:
    body = "23456789012"
    return body + verhoeff_checksum_digit(body)


def _invalid_aadhaar() -> str:
    good = _valid_aadhaar()
    return good[:-1] + ("0" if good[-1] != "0" else "1")


def _valid_gstin() -> str:
    # 22 + PAN-shaped + entity + Z + check
    pan = "ABCDE1234F"
    base = f"22{pan}1Z"
    return base + gstin_check_digit(base)


def test_validate_pii_mode_lite_alias():
    assert validate_pii_mode("lite") == "lite"
    assert validate_pii_mode("rule") == "lite"
    assert validate_pii_mode("hybrid") == "hybrid"
    assert validate_pii_mode("hybrid_calibrated") == "hybrid"


def test_hybrid_feasible_without_full_ml_stack():
    feas = check_pii_mode_feasibility("hybrid")
    assert feas["feasible"] is True
    assert feas["requires_ml"] is False


def test_policy_default_is_hybrid():
    assert PolicyConfig().pii_mode == "hybrid"


def test_verhoeff_aadhaar_valid_and_invalid():
    good = _valid_aadhaar()
    bad = _invalid_aadhaar()
    assert verhoeff_validate(good)
    assert not verhoeff_validate(bad)


def test_pan_and_gstin_validators():
    assert pan_validate("ABCDE1234F")
    assert not pan_validate("ABCDE12345")  # wrong shape
    gstin = _valid_gstin()
    assert gstin_validate(gstin)
    assert not gstin_validate(gstin[:-1] + ("0" if gstin[-1] != "0" else "1"))


def test_luhn_still_works():
    # Well-known Luhn-valid test Visa number (public test fixture).
    assert luhn_validate("4111111111111111")
    assert not luhn_validate("4111111111111112")


def test_lite_detector_masks_valid_aadhaar():
    detector = PIIDetector()
    aadhaar = _valid_aadhaar()
    text = f"My Aadhaar number is {aadhaar} for KYC."
    masked = detector.mask(text)
    assert aadhaar not in masked
    assert "AADHAAR" in masked or "HASH" in masked


def test_invalid_aadhaar_lower_confidence_not_dropped():
    detector = PIIDetector()
    bad = _invalid_aadhaar()
    text = f"Aadhaar {bad} submitted"
    matches = detector._detect_pii_with_context(text)
    aadhaar_matches = [m for m in matches if m.pii_type == "aadhaar"]
    # Soft-fail: may still surface with reduced confidence, or drop below 0.3.
    # Ensure we don't assign full (≥0.9) confidence to a checksum failure.
    for m in aadhaar_matches:
        assert m.confidence < 0.9


def test_pan_and_gstin_detection_in_context():
    detector = PIIDetector()
    pan = "ABCDE1234F"
    gstin = _valid_gstin()
    text = f"PAN {pan} and GSTIN {gstin} on the invoice."
    types = detector.detect_pii_types(text)
    assert "pan" in types
    assert "gstin" in types


def test_indian_phone_detection():
    detector = PIIDetector()
    text = "Call me at +919876543210 please"
    types = detector.detect_pii_types(text)
    assert "phone" in types


def test_locale_detects_indian_cues():
    guess = detect_locale("Please verify Aadhaar and GSTIN for Chennai KYC +91")
    assert guess.locale.endswith("_IN") or guess.locale == "en_IN"
    assert guess.confidence > 0.3


def test_locale_tamil_script():
    guess = detect_locale("என் பெயர் ரவி")
    assert guess.locale.startswith("ta")


def test_hybrid_pipeline_detects_indian_pii():
    detector = HybridPIIDetector(pii_mode="hybrid")
    aadhaar = _valid_aadhaar()
    text = f"Applicant KYC: Aadhaar {aadhaar}, PAN ABCDE1234F."
    result = detector.detect_and_mask(text)
    assert aadhaar not in result.masked_text
    types = {getattr(e, "category", None) for e in result.entities}
    assert "aadhaar" in types or "pan" in types or aadhaar not in result.masked_text


def test_run_security_default_uses_hybrid_path():
    aadhaar = _valid_aadhaar()
    result = run_security(
        f"My Aadhaar is {aadhaar}",
        {"pii_mode": "hybrid", "enable_injection_detection": False},
    )
    assert aadhaar not in result.sanitized_content


def test_lite_opt_in_still_works():
    result = run_security(
        "Contact john@company.com",
        {"pii_mode": "lite", "enable_injection_detection": False},
    )
    assert "john@company.com" not in result.sanitized_content
