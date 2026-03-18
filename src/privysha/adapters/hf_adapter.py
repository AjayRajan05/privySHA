try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from .base import BaseAdapter


class HuggingFaceAdapter(BaseAdapter):

    def __init__(self, model="mistralai/Mistral-7B-Instruct-v0.2"):
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers library is not installed. Install with: pip install transformers torch")
        
        self.model_name = model

        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(
            model,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )

    def generate(self, prompt: str) -> str:
        """Generate response using HuggingFace model."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=True,
            temperature=0.7
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the original prompt from the response
        if response.startswith(prompt):
            response = response[len(prompt):].strip()
        
        return response