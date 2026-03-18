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

from .openai_adapter import OpenAIAdapter
from .ollama_adapter import OllamaAdapter
from .mock_adapter import MockAdapter
from .hf_adapter import HuggingFaceAdapter
from .claude_adapter import ClaudeAdapter

class AdapterFactory:

    @staticmethod
    def create(model_name: str):
        """
        Create adapter based on model name pattern.
        
        Args:
            model_name: Model identifier or provider prefix
            
        Returns:
            Appropriate adapter instance
            
        Examples:
            - "mock" → MockAdapter
            - "gpt-4", "gpt-3.5-turbo" → OpenAIAdapter
            - "claude-3-sonnet", "claude-3-opus" → ClaudeAdapter  
            - "mistralai/Mistral-7B", "microsoft/DialoGPT" → HuggingFaceAdapter
            - "llama2", "codellama" → OllamaAdapter
        """
        
        if model_name.lower() == "mock":
            return MockAdapter(model_name)
        elif model_name.lower().startswith("gpt"):
            try:
                return OpenAIAdapter(model_name)
            except Exception as e:
                print(f"Warning: OpenAI adapter failed ({e}), falling back to mock")
                return MockAdapter(model_name)
        elif model_name.lower().startswith("claude"):
            try:
                return ClaudeAdapter(model_name)
            except Exception as e:
                print(f"Warning: Claude adapter failed ({e}), falling back to mock")
                return MockAdapter(model_name)
        elif "/" in model_name or model_name.lower() in ["mistral", "llama", "phi", "gemma", "bert", "gpt", "t5"]:
            # Assume HuggingFace model (contains org/model format or common model names)
            try:
                return HuggingFaceAdapter(model_name)
            except Exception as e:
                print(f"Warning: HuggingFace adapter failed ({e}), falling back to mock")
                return MockAdapter(model_name)

        # Default to Ollama for local models
        try:
            return OllamaAdapter(model_name)
        except Exception as e:
            print(f"Warning: Ollama adapter failed ({e}), falling back to mock")
            return MockAdapter(model_name)