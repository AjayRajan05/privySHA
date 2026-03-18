import pytest
from unittest.mock import Mock, patch
from privysha import Agent


class TestAgent:
    """Test cases for Agent class."""

    @patch('privysha.adapters.factory.AdapterFactory.create')
    def test_agent_initialization_default_params(self, mock_create):
        """Test Agent initialization with default parameters."""
        mock_adapter = Mock()
        mock_create.return_value = mock_adapter
        
        agent = Agent()
        
        mock_create.assert_called_once_with("llama3")
        assert agent.pipeline is not None
        assert agent.adapter == mock_adapter

    @patch('privysha.adapters.factory.AdapterFactory.create')
    def test_agent_initialization_custom_params(self, mock_create):
        """Test Agent initialization with custom parameters."""
        mock_adapter = Mock()
        mock_create.return_value = mock_adapter
        
        agent = Agent(model="gpt-4", privacy=False, token_budget=2000)
        
        mock_create.assert_called_once_with("gpt-4")
        assert agent.adapter == mock_adapter

    @patch('privysha.adapters.factory.AdapterFactory.create')
    def test_agent_with_gpt_model(self, mock_create):
        """Test Agent creation with GPT model."""
        mock_adapter = Mock()
        mock_create.return_value = mock_adapter
        
        agent = Agent(model="gpt-4")
        
        mock_create.assert_called_once_with("gpt-4")
        assert agent.adapter == mock_adapter

    @patch('privysha.adapters.factory.AdapterFactory.create')
    def test_agent_with_ollama_model(self, mock_create):
        """Test Agent creation with Ollama model."""
        mock_adapter = Mock()
        mock_create.return_value = mock_adapter
        
        agent = Agent(model="llama3")
        
        mock_create.assert_called_once_with("llama3")
        assert agent.adapter == mock_adapter

    @patch('privysha.adapters.factory.AdapterFactory.create')
    def test_agent_run_without_trace(self, mock_create):
        """Test Agent.run() method without trace."""
        mock_adapter = Mock()
        mock_adapter.generate.return_value = "Test response"
        mock_create.return_value = mock_adapter
        
        agent = Agent()
        
        response = agent.run("Test prompt")
        
        assert response == "Test response"
        mock_adapter.generate.assert_called_once()

    @patch('privysha.adapters.factory.AdapterFactory.create')
    def test_agent_run_with_trace(self, mock_create):
        """Test Agent.run() method with trace enabled."""
        mock_adapter = Mock()
        mock_adapter.generate.return_value = "Test response"
        mock_create.return_value = mock_adapter
        
        agent = Agent()
        
        result = agent.run("Test prompt", trace=True)
        
        assert isinstance(result, dict)
        assert "response" in result
        assert result["response"] == "Test response"
        mock_adapter.generate.assert_called_once()

    def test_agent_pipeline_processing(self):
        """Test that pipeline is called during run."""
        agent = Agent()
        
        # Mock the pipeline to verify it's called
        with patch.object(agent.pipeline, 'process') as mock_process:
            mock_process.return_value = {
                "compiled_prompt": "compiled test prompt"
            }
            
            with patch.object(agent.adapter, 'generate') as mock_generate:
                mock_generate.return_value = "response"
                
                agent.run("test prompt")
                
                mock_process.assert_called_once_with("test prompt")
                mock_generate.assert_called_once_with("compiled test prompt")
