class ContextInjector:

    def inject(self, optimized_prompt):

        system_context = (
            "You are an expert data scientist. "
            "Provide precise and analytical responses."
        )

        return {
            "system": system_context,
            "task": optimized_prompt
        }