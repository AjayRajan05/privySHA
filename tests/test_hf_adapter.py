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
    @patch('privysha.adapters.hf_adapter.AutoTokenizer')
    @patch('privysha.adapters.hf_adapter.AutoModelForCausalLM')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_adapter_initialization_default(self, mock_cuda, mock_model, mock_tokenizer):
        """Test adapter initialization with default model."""
        mock_cuda.return_value = False
        mock_tokenizer_instance = Mock()
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        mock_model_instance = Mock()
        mock_model_instance.device = "cpu"
        mock_model.from_pretrained.return_value = mock_model_instance
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter()
        
        assert adapter.model_name == "mistralai/Mistral-7B-Instruct-v0.2"
        mock_tokenizer.from_pretrained.assert_called_once_with("mistralai/Mistral-7B-Instruct-v0.2")
        mock_model.from_pretrained.assert_called_once_with(
            "mistralai/Mistral-7B-Instruct-v0.2",
            torch_dtype="float32",
            device_map="auto"
        )

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('privysha.adapters.hf_adapter.AutoTokenizer')
    @patch('privysha.adapters.hf_adapter.AutoModelForCausalLM')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_adapter_initialization_custom_model(self, mock_cuda, mock_model, mock_tokenizer):
        """Test adapter initialization with custom model."""
        mock_cuda.return_value = True
        mock_tokenizer_instance = Mock()
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        mock_model_instance = Mock()
        mock_model_instance.device = "cuda:0"
        mock_model.from_pretrained.return_value = mock_model_instance
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter("custom/model")
        
        assert adapter.model_name == "custom/model"
        mock_tokenizer.from_pretrained.assert_called_once_with("custom/model")
        mock_model.from_pretrained.assert_called_once_with(
            "custom/model",
            torch_dtype="float16",
            device_map="auto"
        )

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('privysha.adapters.hf_adapter.AutoTokenizer')
    @patch('privysha.adapters.hf_adapter.AutoModelForCausalLM')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_generate_success(self, mock_cuda, mock_model, mock_tokenizer):
        """Test successful prompt generation."""
        mock_cuda.return_value = False
        mock_tokenizer_instance = Mock()
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        mock_model_instance = Mock()
        mock_model_instance.device = "cpu"
        mock_model.from_pretrained.return_value = mock_model_instance
        
        # Mock tokenizer call
        mock_inputs = Mock()
        mock_inputs.to.return_value = mock_inputs
        mock_tokenizer_instance.return_value = mock_inputs
        
        # Mock model generation
        mock_outputs = [Mock()]
        mock_model_instance.generate.return_value = mock_outputs
        
        # Mock tokenizer decode
        mock_tokenizer_instance.decode.return_value = "Test prompt\nGenerated response"
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter()
        result = adapter.generate("Test prompt")
        
        assert result == "Generated response"
        mock_tokenizer_instance.assert_called_with("Test prompt", return_tensors="pt")
        mock_inputs.to.assert_called_with("cpu")
        mock_model_instance.generate.assert_called_once_with(
            mock_inputs,
            max_new_tokens=300,
            do_sample=True,
            temperature=0.7
        )
        mock_tokenizer_instance.decode.assert_called_once_with(mock_outputs[0], skip_special_tokens=True)

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('privysha.adapters.hf_adapter.AutoTokenizer')
    @patch('privysha.adapters.hf_adapter.AutoModelForCausalLM')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_generate_response_without_prompt_prefix(self, mock_cuda, mock_model, mock_tokenizer):
        """Test generation when response doesn't start with prompt."""
        mock_cuda.return_value = False
        mock_tokenizer_instance = Mock()
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        mock_model_instance = Mock()
        mock_model_instance.device = "cpu"
        mock_model.from_pretrained.return_value = mock_model_instance
        
        mock_inputs = Mock()
        mock_inputs.to.return_value = mock_inputs
        mock_tokenizer_instance.return_value = mock_inputs
        
        mock_outputs = [Mock()]
        mock_model_instance.generate.return_value = mock_outputs
        mock_tokenizer_instance.decode.return_value = "Direct response without prompt"
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter()
        result = adapter.generate("Test prompt")
        
        assert result == "Direct response without prompt"

    @patch('privysha.adapters.hf_adapter.TRANSFORMERS_AVAILABLE', True)
    @patch('privysha.adapters.hf_adapter.AutoTokenizer')
    @patch('privysha.adapters.hf_adapter.AutoModelForCausalLM')
    @patch('privysha.adapters.hf_adapter.torch.cuda.is_available')
    def test_generate_empty_prompt(self, mock_cuda, mock_model, mock_tokenizer):
        """Test generation with empty prompt."""
        mock_cuda.return_value = False
        mock_tokenizer_instance = Mock()
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        mock_model_instance = Mock()
        mock_model_instance.device = "cpu"
        mock_model.from_pretrained.return_value = mock_model_instance
        
        mock_inputs = Mock()
        mock_inputs.to.return_value = mock_inputs
        mock_tokenizer_instance.return_value = mock_inputs
        
        mock_outputs = [Mock()]
        mock_model_instance.generate.return_value = mock_outputs
        mock_tokenizer_instance.decode.return_value = "Empty response"
        
        from privysha.adapters.hf_adapter import HuggingFaceAdapter
        adapter = HuggingFaceAdapter()
        result = adapter.generate("")
        
        assert result == "Empty response"
