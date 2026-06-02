from qdrant_client import QdrantClient

from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)


class QDrantDB:

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        distance_metric: str = "cosine"
    ):

        self.client = QdrantClient(
            host=host,
            port=port
        )

        self.distance_metric = (
            Distance.COSINE
            if distance_metric.lower() == "cosine"
            else Distance.EUCLID
        )


    def create_collection(
    self,
    collection_name: str,
    embedding_size: int
    ):
        self.client.recreate_collection(
            collection_name=collection_name,

            vectors_config=VectorParams(
                size=embedding_size,
                distance=self.distance_metric
            )
        )


    def add_documents(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list
    ):

        points = []

        for index, vector in enumerate(vectors):

            points.append(
                PointStruct(
                    id=index,
                    vector=vector,

                    payload={
                        "text": texts[index],
                        "metadata": metadata[index]
                    }
                )
            )

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )


    def search_by_vector(
        self,
        collection_name: str,
        query_vector: list,
        top_k: int
    ):

        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
        )

        return [
            {
                "text": result.payload.get(
                    "text",
                    ""
                ),

                "score": float(result.score),

                "metadata": result.payload.get(
                    "metadata",
                    {}
                ),
            }

            for result in results
        ]


    def delete_collection(
        self,
        collection_name: str
    ):

        self.client.delete_collection(
            collection_name
        )


    def is_collection_exists(
        self,
        collection_name: str
    ):

        return self.client.collection_exists(
            collection_name
        )