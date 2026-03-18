import pytest
from unittest.mock import Mock, patch
from privysha.adapters.factory import AdapterFactory
from privysha.adapters.openai_adapter import OpenAIAdapter
from privysha.adapters.ollama_adapter import OllamaAdapter


class TestAdapterFactory:
    """Test cases for AdapterFactory class."""

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_create_gpt_model(self, mock_getenv, mock_openai):
        """Test factory creates OpenAI adapter for GPT models."""
        mock_getenv.return_value = "test-api-key"
        adapter = AdapterFactory.create("gpt-4")
        
        assert isinstance(adapter, OpenAIAdapter)
        assert adapter.model == "gpt-4"

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_create_gpt_model_variations(self, mock_getenv, mock_openai):
        """Test factory creates OpenAI adapter for various GPT model names."""
        mock_getenv.return_value = "test-api-key"
        gpt_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini", "gpt-4-turbo"]
        
        for model in gpt_models:
            adapter = AdapterFactory.create(model)
            assert isinstance(adapter, OpenAIAdapter)
            assert adapter.model == model

    def test_create_ollama_model(self):
        """Test factory creates Ollama adapter for non-GPT models."""
        adapter = AdapterFactory.create("llama3")
        
        assert isinstance(adapter, OllamaAdapter)
        assert adapter.model == "llama3"

    def test_create_ollama_model_variations(self):
        """Test factory creates Ollama adapter for various non-GPT models."""
        ollama_models = ["llama3", "mistral", "codellama", "qwen"]
        
        for model in ollama_models:
            adapter = AdapterFactory.create(model)
            assert isinstance(adapter, OllamaAdapter)
            assert adapter.model == model

    def test_create_empty_model(self):
        """Test factory handles empty model name."""
        adapter = AdapterFactory.create("")
        
        assert isinstance(adapter, OllamaAdapter)
        assert adapter.model == ""

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_create_case_sensitive(self, mock_getenv, mock_openai):
        """Test factory is case sensitive for model names."""
        mock_getenv.return_value = "test-api-key"
        # GPT models should be case sensitive
        adapter = AdapterFactory.create("GPT-4")
        assert isinstance(adapter, OllamaAdapter)  # Should not match "gpt"
        
        adapter = AdapterFactory.create("gpt-4")
        assert isinstance(adapter, OpenAIAdapter)

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_create_partial_gpt_name(self, mock_getenv, mock_openai):
        """Test factory handles partial GPT names."""
        mock_getenv.return_value = "test-api-key"
        # Models that start with "gpt" should use OpenAI adapter
        adapter = AdapterFactory.create("gpt")
        assert isinstance(adapter, OpenAIAdapter)
        
        adapter = AdapterFactory.create("gpt-custom")
        assert isinstance(adapter, OpenAIAdapter)
        
        # Models that don't start with "gpt" should use Ollama adapter
        adapter = AdapterFactory.create("my-gpt-model")
        assert isinstance(adapter, OllamaAdapter)
