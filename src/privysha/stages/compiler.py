class Compiler:

    def compile(self, context):

        system = context["system"]
        task = context["task"]

        final_prompt = f"""
SYSTEM:
{system}

TASK:
{task}
"""

        return final_prompt.strip()