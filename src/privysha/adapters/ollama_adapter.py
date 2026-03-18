import requests
from .base import BaseAdapter


class OllamaAdapter(BaseAdapter):

    def __init__(self, model="llama3"):
        self.model = model

    def generate(self, prompt):

        url = "http://localhost:11434/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        r = requests.post(url, json=payload)

        return r.json()["response"]