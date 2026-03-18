from .openai_adapter import OpenAIAdapter
from .ollama_adapter import OllamaAdapter
from .mock_adapter import MockAdapter


class AdapterFactory:

    @staticmethod
    def create(model_name: str):

        if model_name == "mock":
            return MockAdapter(model_name)
        elif model_name.startswith("gpt"):
            return OpenAIAdapter(model_name)

        return OllamaAdapter(model_name)