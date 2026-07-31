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

"""
ASHA - Drop-in Security & Optimization Layer for Any LLM App

Primary API (import directly):
    from asha import process, sanitize, optimize, Agent

Advanced components live in subpackages:
    from asha.runtime import PromptProcessor
    from asha.integrations import wrap_llm
    from asha.types import ProcessResult

Package ``__init__`` is intentionally lazy: importing ``asha.core.text`` must
not pull Agent / drop-in / ANCHOR (keeps Base cold-import in the low hundreds
of ms). Public names resolve via ``__getattr__``.
"""

from __future__ import annotations

from typing import Any

__version__ = "0.4.2"

__all__ = [
    "__version__",
    "process",
    "sanitize",
    "optimize",
    "Agent",
    "anchor",
]


def __getattr__(name: str) -> Any:
    if name == "Agent":
        from .runtime.agent import Agent

        return Agent
    if name == "anchor":
        from .runtime.anchor.runtime import anchor

        return anchor
    if name in ("process", "sanitize", "optimize"):
        from .utils.dropin import optimize, process, sanitize

        mapping = {
            "process": process,
            "sanitize": sanitize,
            "optimize": optimize,
        }
        return mapping[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
