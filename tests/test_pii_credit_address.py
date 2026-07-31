"""PII detection tests for credit cards and addresses."""

from asha.core.policy_config import PolicyConfig
from asha.core.security.pii_detector import PIIDetector
from asha.core.pii_pipeline.components.detectors.regex_detector import RegexDetector
from asha.utils.dropin import sanitize

from conftest import output_of


VALID_VISA = "4111111111111111"
VALID_VISA_SPACED = "4111 1111 1111 1111"
INVALID_LUHN = "4111111111111112"


class TestCreditCardLuhn:
    def test_valid_card_detected(self):
        detector = PIIDetector()
        types = detector.detect_pii_types(f"Pay with {VALID_VISA}")
        assert "credit_card" in types

    def test_invalid_luhn_rejected_by_detector(self):
        detector = PIIDetector()
        types = detector.detect_pii_types(f"ID {INVALID_LUHN}")
        assert "credit_card" not in types

    def test_regex_detector_luhn_soft_fail(self):
        """Checksum failure lowers confidence; does not grant full confidence."""
        regex = RegexDetector()
        valid = regex.detect(f"Card: {VALID_VISA_SPACED}")
        invalid = regex.detect(f"Ref: {INVALID_LUHN}")
        assert any(e.pii_type == "credit_card" for e in valid)
        valid_cc = [e for e in valid if e.pii_type == "credit_card"]
        assert all(e.metadata.get("checksum_valid") for e in valid_cc)
        invalid_cc = [e for e in invalid if e.pii_type == "credit_card"]
        for e in invalid_cc:
            assert e.metadata.get("checksum_valid") is False
            assert e.confidence < valid_cc[0].confidence

    def test_sanitize_masks_valid_card(self):
        # Exact hash-token format is the lite/PIIDetector path.
        out = output_of(
            sanitize(
                f"My card is {VALID_VISA}",
                policy=PolicyConfig(pii_mode="lite"),
            )
        )
        assert VALID_VISA not in out
        assert "[CREDIT_CARD_HASH]" in out

    def test_sanitize_masks_spaced_card(self):
        out = output_of(
            sanitize(
                f"Charge {VALID_VISA_SPACED} please",
                policy=PolicyConfig(pii_mode="lite"),
            )
        )
        assert VALID_VISA not in out.replace(" ", "")


class TestAddressDetection:
    def test_street_suffix_detected(self):
        detector = PIIDetector()
        text = "Office at 500 Main Street, Boston"
        types = detector.detect_pii_types(text)
        assert "address" in types

    def test_sanitize_masks_street_address(self):
        out = output_of(
            sanitize(
                "Ship to 742 Evergreen Street today",
                policy=PolicyConfig(pii_mode="lite"),
            )
        )
        assert "742 Evergreen Street" not in out
        assert "[ADDRESS_HASH]" in out

    def test_process_masks_full_address(self):
        from asha import process

        text = "Office at 100 Oak Avenue, Springfield, IL 62701"
        out = output_of(process(text, mode="strict"))
        assert "Oak Avenue" not in out or "[ADDRESS_HASH]" in out

    def test_address_hash_token_in_output(self):
        out = output_of(
            sanitize(
                "Located at 42 Maple Drive",
                policy=PolicyConfig(pii_mode="lite"),
            )
        )
        assert "[ADDRESS_HASH]" in out
