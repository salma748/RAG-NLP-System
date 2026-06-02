from stores.vectordb.provider.QDrantDB import QDrantDB
class VectorDBFactory:

    @staticmethod
    def create(
        provider: str,
        **kwargs
    ):

        if provider.lower() == "qdrant":

            return QDrantDB(
                host=kwargs.get("host", "localhost"),
                port=kwargs.get("port", 6333),
                distance_metric=kwargs.get(
                    "distance_metric",
                    "cosine"
                )
            )

        raise ValueError(
            f"Unsupported vector DB provider: {provider}"
        )