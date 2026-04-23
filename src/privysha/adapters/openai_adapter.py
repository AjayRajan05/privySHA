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

import os
from openai import OpenAI
from .base import BaseAdapter
from .universal_adapter import UniversalModelAdapter


class OpenAIAdapter(BaseAdapter):
    """
    OpenAI Adapter - Backward compatible wrapper using UniversalModelAdapter.
    """

    def __init__(self, model="gpt-4o-mini"):
        """Initialize using universal adapter for better functionality."""
        self._adapter = UniversalModelAdapter(
            provider="openai",
            model=model,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = model

    def generate(self, prompt: str) -> str:
        """Generate response using universal adapter."""
        return self._adapter.generate(prompt)

    # Additional v2 methods exposed for compatibility
    def generate_with_fallback(self, prompt: str, fallback_models=None) -> str:
        """Generate with fallback support."""
        return self._adapter.generate_with_fallback(prompt, fallback_models)

    def get_provider_info(self) -> dict:
        """Get provider information."""
        return self._adapter.get_provider_info()