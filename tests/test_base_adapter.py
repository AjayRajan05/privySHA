import pytest
from privysha.adapters.base import BaseAdapter


class TestBaseAdapter:
    """Test cases for BaseAdapter abstract class."""

    def test_base_adapter_is_abstract(self):
        """Test that BaseAdapter cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseAdapter()

    def test_concrete_adapter_implementation(self):
        """Test that concrete implementation of BaseAdapter works."""
        
        class ConcreteAdapter(BaseAdapter):
            def generate(self, prompt: str) -> str:
                return f"Processed: {prompt}"
        
        adapter = ConcreteAdapter()
        result = adapter.generate("test prompt")
        
        assert result == "Processed: test prompt"

    def test_base_adapter_has_abstract_method(self):
        """Test that BaseAdapter has abstract generate method."""
        assert hasattr(BaseAdapter, 'generate')
        # Check if the method is abstract by looking at the class definition
        from abc import ABC
        assert issubclass(BaseAdapter, ABC)

    def test_concrete_adapter_method_signature(self):
        """Test that concrete adapter matches expected method signature."""
        
        class ConcreteAdapter(BaseAdapter):
            def generate(self, prompt: str) -> str:
                return prompt
        
        adapter = ConcreteAdapter()
        
        # Test method accepts string parameter
        result = adapter.generate("test")
        assert result == "test"
        
        # Test method returns string
        assert isinstance(result, str)
