class Optimizer:

    def __init__(self, token_budget=1200):
        self.token_budget = token_budget

    def compress(self, text):

        words = text.split()

        if len(words) > 10:
            words = words[:10]

        return " ".join(words)

    def run(self, text):

        compressed = self.compress(text)

        if "analyze" in compressed and "dataset" in compressed:
            return "@analyze(dataset)"

        return compressed