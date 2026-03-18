import re
from ..utils.pii_detector import PIIDetector


class Sanitizer:

    def __init__(self, privacy=True):
        self.privacy = privacy
        self.pii = PIIDetector()

        self.filler_words = [
            "hey",
            "bro",
            "please",
            "can you",
            "could you"
        ]

    def remove_fillers(self, text):

        for word in self.filler_words:
            text = text.replace(word, "")

        return text.strip()

    def run(self, prompt):

        cleaned = prompt.lower()

        cleaned = self.remove_fillers(cleaned)

        if self.privacy:
            cleaned = self.pii.mask(cleaned)

        cleaned = re.sub(r"\s+", " ", cleaned)

        return cleaned