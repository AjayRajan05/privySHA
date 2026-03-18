from .pipeline import Pipeline
from .adapters.factory import AdapterFactory


class Agent:

    def __init__(self, model="llama3", privacy=True, token_budget=1200):

        self.pipeline = Pipeline(
            privacy=privacy,
            token_budget=token_budget
        )

        self.adapter = AdapterFactory.create(model)

    def run(self, prompt: str, trace=False):

        result = self.pipeline.process(prompt)

        response = self.adapter.generate(result["compiled_prompt"])

        if trace:
            result["response"] = response
            return result

        return response