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

    def optimize(self, ir):
        # Apply optimization rules
        if hasattr(ir, 'copy'):
            optimized_ir = ir.copy()
        else:
            # Handle case where ir is a dict
            optimized_ir = ir.copy() if isinstance(ir, dict) else ir
        
        # Remove redundant constraints if they exist
        if hasattr(optimized_ir, 'constraints'):
            if "thorough" in optimized_ir.constraints and "detailed" in optimized_ir.constraints:
                optimized_ir.constraints.remove("detailed")
        elif isinstance(optimized_ir, dict) and "constraints" in optimized_ir:
            if "thorough" in optimized_ir["constraints"] and "detailed" in optimized_ir["constraints"]:
                optimized_ir["constraints"].remove("detailed")
        
        return optimized_ir

    def compress(self, text):
        if not isinstance(text, str):
            text = str(text)
        
        words = text.split()

        if len(words) > 10:
            words = words[:10]

        return " ".join(words)

    def run(self, text):
        if not isinstance(text, str):
            text = str(text)

        compressed = self.compress(text)

        if "analyze" in compressed and "dataset" in compressed:
            return "@analyze(dataset)"

        return compressed