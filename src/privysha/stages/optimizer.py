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