import re


class PIIDetector:

    def mask(self, text):

        text = re.sub(
            r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "<EMAIL_HASH>",
            text
        )

        text = re.sub(
            r"\+?\d[\d -]{8,12}\d",
            "<PHONE_HASH>",
            text
        )

        return text