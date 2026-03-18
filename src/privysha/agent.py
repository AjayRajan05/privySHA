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