import pytest
from privysha.adapters.model_adapter import ModelAdapter


class TestModelAdapter:
    """Test cases for ModelAdapter class."""

    def test_adapter_initialization_default(self):
        """Test adapter initialization with default model."""
        adapter = ModelAdapter()
        
        assert adapter.model == "mock"

    def test_adapter_initialization_custom_model(self):
        """Test adapter initialization with custom model."""
        adapter = ModelAdapter("custom-model")
        
        assert adapter.model == "custom-model"

    def test_generate_default_model(self):
        """Test prompt generation with default model."""
        adapter = ModelAdapter()
        result = adapter.generate("Test prompt")
        
        expected = "[mock RESPONSE]\nProcessed Prompt:\nTest prompt"
        assert result == expected

    def test_generate_custom_model(self):
        """Test prompt generation with custom model."""
        adapter = ModelAdapter("gpt-4")
        result = adapter.generate("Test prompt")
        
        expected = "[gpt-4 RESPONSE]\nProcessed Prompt:\nTest prompt"
        assert result == expected

    def test_generate_empty_prompt(self):
        """Test prompt generation with empty prompt."""
        adapter = ModelAdapter()
        result = adapter.generate("")
        
        expected = "[mock RESPONSE]\nProcessed Prompt:\n"
        assert result == expected

    def test_generate_long_prompt(self):
        """Test prompt generation with long prompt."""
        long_prompt = "This is a very long prompt " * 100
        adapter = ModelAdapter()
        result = adapter.generate(long_prompt)
        
        expected = f"[mock RESPONSE]\nProcessed Prompt:\n{long_prompt}"
        assert result == expected

    def test_generate_with_special_characters(self):
        """Test prompt generation with special characters."""
        special_prompt = "Test prompt with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        adapter = ModelAdapter()
        result = adapter.generate(special_prompt)
        
        expected = f"[mock RESPONSE]\nProcessed Prompt:\n{special_prompt}"
        assert result == expected

    def test_generate_multiline_prompt(self):
        """Test prompt generation with multiline prompt."""
        multiline_prompt = "Line 1\nLine 2\nLine 3"
        adapter = ModelAdapter()
        result = adapter.generate(multiline_prompt)
        
        expected = f"[mock RESPONSE]\nProcessed Prompt:\n{multiline_prompt}"
        assert result == expected
