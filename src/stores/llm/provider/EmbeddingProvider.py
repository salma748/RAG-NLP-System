from sentence_transformers import SentenceTransformer


class EmbeddingProvider:

    def __init__(
        
        self,
        model_name: str = (
            "BAAI/bge-m3"
        )
    ):

        self.model = SentenceTransformer(
            model_name
        )

        self.embedding_size = (
            self.model.get_sentence_embedding_dimension()
        )


    def embed(
        self,
        text: str,
        doc_type: str = "passage"
    ):

        # Clean text
        text = text.strip()

        # Asymmetric embedding prompts
        if doc_type == "query":

            text = (
                "Represent this search query for retrieval: "
                f"{text}"
            )

        else:

            text = (
                "Represent this document for retrieval: "
                f"{text}"
            )

        vector = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return vector.tolist()