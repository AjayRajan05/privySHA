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

"""Optional framework dependency helpers for ANCHOR adapters."""

from __future__ import annotations

from typing import Optional


_EXTRA_HINTS = {
    "crewai": "pip install asha[crewai]",
    "langchain": "pip install asha[langchain]",
    "langchain_core": "pip install asha[langchain]",
    "langgraph": "pip install asha[langgraph]",
    "llama_index": "pip install asha[llamaindex]",
    "mcp": "pip install asha[mcp]",
}


def missing_extra_error(package: str, *, adapter: Optional[str] = None) -> ImportError:
    """Build a clear ImportError pointing at the right ``asha[...]`` extra."""
    hint = _EXTRA_HINTS.get(package, f"pip install {package}")
    where = f" for {adapter}" if adapter else ""
    return ImportError(
        f"Optional dependency '{package}' is required{where}. Install with: {hint}"
    )


def require_module(module_name: str, *, adapter: str) -> None:
    """Import ``module_name`` or raise :func:`missing_extra_error`."""
    try:
        __import__(module_name)
    except ImportError as exc:
        root = module_name.split(".", 1)[0]
        raise missing_extra_error(root, adapter=adapter) from exc
