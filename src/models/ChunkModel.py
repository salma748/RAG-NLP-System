class ChunkModel:

    def __init__(self, db_client):

        self.collection = db_client["chunks"]


    async def insert_many_chunks(
        self,
        project_id: str,
        chunks: list
    ):

        if not chunks:
            return 0

        documents = []

        for index, chunk in enumerate(chunks):

            documents.append({
                "project_id": project_id,
                "chunk_text": chunk,
                "chunk_order": index,
                "chunk_length": len(chunk),
            })

        result = await self.collection.insert_many(documents)

        return len(result.inserted_ids)


    async def get_chunks_by_project_id(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 100
    ):

        chunks = []

        cursor = self.collection.find({
            "project_id": project_id,
        }).sort(
            "chunk_order",
            1
        ).skip(skip).limit(limit)

        async for chunk in cursor:

            chunks.append(chunk)

        return chunks


    async def delete_chunks_by_project_id(
        self,
        project_id: str
    ):

        result = await self.collection.delete_many({
            "project_id": project_id,
        })

        return result.deleted_count