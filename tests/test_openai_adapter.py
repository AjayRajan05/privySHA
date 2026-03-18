import pytest
from unittest.mock import Mock, patch, MagicMock
from privysha.adapters.openai_adapter import OpenAIAdapter


class TestOpenAIAdapter:
    """Test cases for OpenAIAdapter class."""

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_adapter_initialization_default(self, mock_getenv, mock_openai):
        """Test adapter initialization with default model."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        adapter = OpenAIAdapter()
        
        mock_openai.assert_called_once_with(api_key="test-api-key")
        mock_getenv.assert_called_once_with("OPENAI_API_KEY")
        assert adapter.model == "gpt-4o-mini"
        assert adapter.client == mock_client

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_adapter_initialization_custom_model(self, mock_getenv, mock_openai):
        """Test adapter initialization with custom model."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        adapter = OpenAIAdapter("gpt-4")
        
        mock_openai.assert_called_once_with(api_key="test-api-key")
        assert adapter.model == "gpt-4"

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_generate_success(self, mock_getenv, mock_openai):
        """Test successful prompt generation."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock the response structure
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Generated response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response
        
        adapter = OpenAIAdapter()
        result = adapter.generate("Test prompt")
        
        assert result == "Generated response"
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Test prompt"}
            ]
        )

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_generate_with_custom_model(self, mock_getenv, mock_openai):
        """Test prompt generation with custom model."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Custom model response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response
        
        adapter = OpenAIAdapter("gpt-4")
        result = adapter.generate("Test prompt")
        
        assert result == "Custom model response"
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4",
            messages=[
                {"role": "user", "content": "Test prompt"}
            ]
        )

    @patch('privysha.adapters.openai_adapter.OpenAI')
    @patch('privysha.adapters.openai_adapter.os.getenv')
    def test_generate_empty_prompt(self, mock_getenv, mock_openai):
        """Test prompt generation with empty prompt."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = ""
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response
        
        adapter = OpenAIAdapter()
        result = adapter.generate("")
        
        assert result == ""
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": ""}
            ]
        )
