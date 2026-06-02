class LLMInterface:

    def generate_response(
        self,
        prompt: str,
        chat_history: list
    ):
        raise NotImplementedError