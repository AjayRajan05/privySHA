# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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