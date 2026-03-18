from .base import BaseAdapter


class ModelAdapter(BaseAdapter):

    def __init__(self, model="mock"):
        self.model = model

    def generate(self, prompt: str) -> str:
        """Generate mock response for testing purposes."""
        # placeholder model execution
        return f"[{self.model} RESPONSE]\nProcessed Prompt:\n{prompt}"