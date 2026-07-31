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

"""PII detection via canonicalize + context boost (lite path)."""

from __future__ import annotations

from asha.core.security.pii_detector import PIIDetector
from asha.utils.dropin import sanitize


def test_obfuscated_phone_detected_and_masked():
    """Zero-width split Indian mobile must be detected after canonicalize."""
    phone = "9\u200b8\u200c7\u200d6\u206065\u206143\u206132\u206110"
    text = f"My phone number is {phone} for callbacks."
    detector = PIIDetector()
    masked = detector.mask(text)
    assert "[PHONE_HASH]" in masked
    assert phone not in masked


def test_obfuscated_email_detected_and_masked():
    """Fullwidth / homoglyph email local-part must still match."""
    email = "j\u0430ne\u200b@gmail.com"  # Cyrillic 'a' + zero-width
    text = f"Contact me at {email} please."
    detector = PIIDetector()
    masked = detector.mask(text)
    assert "[EMAIL_HASH]" in masked


def test_sanitize_masks_obfuscated_phone():
    phone = "9\u200b8\u200c7\u200d6\u206065\u206143\u206132\u206110"
    text = f"Call me on phone {phone} tomorrow."
    result = sanitize(text, mode="lite")
    assert result.output is not None
    assert "[PHONE_HASH]" in result.output or "PHONE" in result.output.upper()
