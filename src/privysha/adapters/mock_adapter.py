from .base import BaseAdapter


class MockAdapter(BaseAdapter):
    """Mock adapter for testing purposes without requiring external LLM services"""

    def __init__(self, model="mock"):
        self.model = model

    def generate(self, prompt):
        """Generate a mock response based on the prompt content"""
        
        # Simple mock responses based on prompt content
        if "analyze" in prompt.lower():
            return "Mock analysis completed. Found patterns in the data."
        elif "dataset" in prompt.lower():
            return "Mock dataset processing complete."
        elif "anomalies" in prompt.lower():
            return "Mock anomaly detection finished. No anomalies detected."
        else:
            return "Mock response: Processing completed successfully."
        
        # In a real implementation, this would call an LLM API
        # return f"Mock response for: {prompt[:50]}..."
