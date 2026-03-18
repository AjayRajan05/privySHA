class PromptParser:

    def parse(self, prompt: str):

        words = prompt.lower().split()

        intent = None
        object_ = None

        if "analyze" in words:
            intent = "analyze"

        if "dataset" in words:
            object_ = "dataset"

        return {
            "intent": intent,
            "object": object_
        }