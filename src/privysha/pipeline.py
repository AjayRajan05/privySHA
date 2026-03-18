from .parser.prompt_ast import PromptParser
from .stages.sanitizer import Sanitizer
from .stages.optimizer import Optimizer
from .stages.compiler import Compiler
from .stages.context import ContextInjector


class Pipeline:

    def __init__(self, privacy=True, token_budget=1200):

        self.parser = PromptParser()
        self.sanitizer = Sanitizer(privacy)
        self.optimizer = Optimizer(token_budget)
        self.context = ContextInjector()
        self.compiler = Compiler()

    def process(self, prompt):

        trace = {}

        trace["raw_prompt"] = prompt

        ast = self.parser.parse(prompt)
        trace["ast"] = ast

        sanitized = self.sanitizer.run(prompt)
        trace["sanitized"] = sanitized

        optimized = self.optimizer.run(sanitized)
        trace["optimized"] = optimized

        contextual = self.context.inject(optimized)
        trace["context"] = contextual

        compiled = self.compiler.compile(contextual)
        trace["compiled_prompt"] = compiled

        return trace