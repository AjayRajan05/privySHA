import pytest
from unittest.mock import Mock, patch, MagicMock
from privysha.adapters.ollama_adapter import OllamaAdapter


class TestOllamaAdapter:
    """Test cases for OllamaAdapter class."""

    def test_adapter_initialization_default(self):
        """Test adapter initialization with default model."""
        adapter = OllamaAdapter()
        
        assert adapter.model == "llama3"

    def test_adapter_initialization_custom_model(self):
        """Test adapter initialization with custom model."""
        adapter = OllamaAdapter("mistral")
        
        assert adapter.model == "mistral"

    @patch('privysha.adapters.ollama_adapter.requests.post')
    def test_generate_success(self, mock_post):
        """Test successful prompt generation."""
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "Generated response",
            "done": True
        }
        mock_post.return_value = mock_response
        
        adapter = OllamaAdapter()
        result = adapter.generate("Test prompt")
        
        assert result == "Generated response"
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": "Test prompt",
                "stream": False
            }
        )

    @patch('privysha.adapters.ollama_adapter.requests.post')
    def test_generate_with_custom_model(self, mock_post):
        """Test prompt generation with custom model."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "Custom model response",
            "done": True
        }
        mock_post.return_value = mock_response
        
        adapter = OllamaAdapter("mistral")
        result = adapter.generate("Test prompt")
        
        assert result == "Custom model response"
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": "Test prompt",
                "stream": False
            }
        )

    @patch('privysha.adapters.ollama_adapter.requests.post')
    def test_generate_empty_prompt(self, mock_post):
        """Test prompt generation with empty prompt."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "",
            "done": True
        }
        mock_post.return_value = mock_response
        
        adapter = OllamaAdapter()
        result = adapter.generate("")
        
        assert result == ""
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": "",
                "stream": False
            }
        )

    @patch('privysha.adapters.ollama_adapter.requests.post')
    def test_generate_long_prompt(self, mock_post):
        """Test prompt generation with long prompt."""
        long_prompt = "This is a very long prompt " * 100
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "Long response",
            "done": True
        }
        mock_post.return_value = mock_response
        
        adapter = OllamaAdapter()
        result = adapter.generate(long_prompt)
        
        assert result == "Long response"
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": long_prompt,
                "stream": False
            }
        )

    @patch('privysha.adapters.ollama_adapter.requests.post')
    def test_generate_with_special_characters(self, mock_post):
        """Test prompt generation with special characters."""
        special_prompt = "Test prompt with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "Special chars response",
            "done": True
        }
        mock_post.return_value = mock_response
        
        adapter = OllamaAdapter()
        result = adapter.generate(special_prompt)
        
        assert result == "Special chars response"
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": special_prompt,
                "stream": False
            }
        )
