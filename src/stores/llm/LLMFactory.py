from stores.llm.provider.OpenAIProvider import OpenAIProvider
from stores.llm.provider.EmbeddingProvider import EmbeddingProvider


class LLMFactory:

    @staticmethod
    def create(
        provider: str,
        **kwargs
    ):

        if provider.lower() == "openai":

            return OpenAIProvider(
                api_key=kwargs.get("api_key"),
                api_base=kwargs.get("api_base"),
                model_name=kwargs.get("model_name"),
                max_response_tokens=kwargs.get(
                    "max_response_tokens",
                    500
                ),
                temperature=kwargs.get(
                    "temperature",
                    0.1
                ),
            )

        elif provider.lower() == "local_bge":

            return EmbeddingProvider(
                model_name=kwargs.get("model_name")
            )

        raise ValueError(
            f"Unsupported provider: {provider}"
        )