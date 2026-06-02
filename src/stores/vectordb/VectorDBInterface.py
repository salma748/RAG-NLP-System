class VectorDBInterface:

    def create_collection(
        self,
        collection_name: str,
        vector_size: int
    ):
        raise NotImplementedError


    def add_documents(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list
    ):
        raise NotImplementedError


    def search_by_vector(
        self,
        collection_name: str,
        query_vector: list,
        top_k: int
    ):
        raise NotImplementedError


    def delete_collection(
        self,
        collection_name: str
    ):
        raise NotImplementedError


    def is_collection_exists(
        self,
        collection_name: str
    ):
        raise NotImplementedError