import pytest
from unittest.mock import Mock, patch, MagicMock


class TestHuggingFaceAdapter:
    """Test cases for HuggingFaceAdapter class."""

    def test_adapter_import_error(self):
        """Test adapter initialization when transformers is not available."""
        with patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', False):
            from privysha.adapters.hf_adapter import HuggingFaceAdapter
            
            with pytest.raises(ImportError, match="transformers library is not installed"):
                HuggingFaceAdapter()

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('transformers.pipeline')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_adapter_initialization_default(self, mock_cuda, mock_pipeline):
        """Test adapter initialization with default model."""
        mock_cuda.return_value = False
        mock_generator = Mock()
        mock_pipeline.return_value = mock_generator
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter("mistralai/Mistral-7B-Instruct-v0.2")
        
        assert adapter.model_name == "mistralai/Mistral-7B-Instruct-v0.2"
        mock_pipeline.assert_called_once_with(
            "text-generation",
            model="mistralai/Mistral-7B-Instruct-v0.2",
            torch_dtype="float32",
            device=-1,
            trust_remote_code=True
        )

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('transformers.pipeline')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_adapter_initialization_custom_model(self, mock_cuda, mock_pipeline):
        """Test adapter initialization with custom model."""
        mock_cuda.return_value = True
        mock_generator = Mock()
        mock_pipeline.return_value = mock_generator
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter("custom/model")
        
        assert adapter.model_name == "custom/model"
        mock_pipeline.assert_called_once_with(
            "text-generation",
            model="custom/model",
            torch_dtype="float16",
            device=0,
            trust_remote_code=True
        )

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('transformers.pipeline')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_generate_success(self, mock_cuda, mock_pipeline):
        """Test successful prompt generation."""
        mock_cuda.return_value = False
        mock_generator = Mock()
        mock_pipeline.return_value = mock_generator
        
        # Mock pipeline generation
        mock_outputs = [{"generated_text": "Generated response"}]
        mock_generator.return_value = mock_outputs
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter("mistralai/Mistral-7B-Instruct-v0.2")
        result = adapter.generate("Test prompt")
        
        assert result == "Generated response"
        mock_generator.assert_called_once_with(
            "Test prompt",
            max_new_tokens=300,
            do_sample=True,
            temperature=0.7,
            pad_token_id=mock_generator.tokenizer.eos_token_id,
            return_full_text=False
        )

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('transformers.pipeline')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_generate_response_without_prompt_prefix(self, mock_cuda, mock_pipeline):
        """Test generation when response doesn't start with prompt."""
        mock_cuda.return_value = False
        mock_generator = Mock()
        mock_pipeline.return_value = mock_generator
        
        mock_outputs = [{"generated_text": "Direct response without prompt"}]
        mock_generator.return_value = mock_outputs
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter("mistralai/Mistral-7B-Instruct-v0.2")
        result = adapter.generate("Test prompt")
        
        assert result == "Direct response without prompt"

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('transformers.pipeline')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_generate_empty_prompt(self, mock_cuda, mock_pipeline):
        """Test generation with empty prompt."""
        mock_cuda.return_value = False
        mock_generator = Mock()
        mock_pipeline.return_value = mock_generator
        
        mock_outputs = [{"generated_text": "Empty response"}]
        mock_generator.return_value = mock_outputs
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter("mistralai/Mistral-7B-Instruct-v0.2")
        result = adapter.generate("")
        
        assert result == "Empty response"
