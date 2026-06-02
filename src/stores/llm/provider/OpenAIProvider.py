from openai import OpenAI


class OpenAIProvider:

    def __init__(
        self,
        api_key: str,
        api_base: str,
        model_name: str,
        max_response_tokens: int = 500,
        temperature: float = 0.1,
    ):

        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base,
        )

        self.model_name = model_name
        self.max_response_tokens = max_response_tokens
        self.temperature = temperature


    def construct_prompt(
        self,
        query: str,
        role: str = "user"
    ):

        return {
            "role": role,
            "content": query,
        }


    def generate_response(
        self,
        prompt: str,
        chat_history: list
    ):

        messages = chat_history + [
            self.construct_prompt(
                query=prompt,
                role="user",
            )
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_response_tokens,
        )

        return (
            response.choices[0]
            .message.content
            .strip()
        )