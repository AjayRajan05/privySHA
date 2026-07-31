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

"""Shared classical ML/DL helpers for ASHA detection hardening.

Heavy dependencies (sentence-transformers, sklearn, lightgbm, …) are
lazy-imported inside call paths so ``import asha`` stays lite.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "EmbeddingEncoder",
    "get_encoder",
    "ThresholdBands",
    "Verdict",
    "bucket_probability",
    "load_thresholds",
    "fit_and_serialize_calibrator",
    "load_calibrator",
    "calibrated_predict_proba",
    "derive_threshold_at_fpr",
    "shannon_entropy",
    "scan_secrets",
    "SecretHit",
]


def __getattr__(name: str) -> Any:
    if name in ("EmbeddingEncoder", "get_encoder"):
        from .embeddings import EmbeddingEncoder, get_encoder

        return {"EmbeddingEncoder": EmbeddingEncoder, "get_encoder": get_encoder}[name]
    if name in (
        "ThresholdBands",
        "Verdict",
        "bucket_probability",
        "load_thresholds",
        "fit_and_serialize_calibrator",
        "load_calibrator",
        "calibrated_predict_proba",
        "derive_threshold_at_fpr",
    ):
        from . import calibration as _cal

        return getattr(_cal, name)
    if name in ("shannon_entropy", "scan_secrets", "SecretHit"):
        from . import secret_entropy as _se

        return getattr(_se, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
