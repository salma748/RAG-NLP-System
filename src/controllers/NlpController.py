import asyncio

from helpers.config import get_settings
from models.ChunkModel import ChunkModel


class NlpController:

    def __init__(
        self,
        vectordb_client,
        generation_client,
        embedding_client,
        template_parser
    ):

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser


    # Collection Name

    def create_collection_name(
        self,
        project_id: str
    ):

        return f"collection_{project_id}"


    # Push Chunks To Qdrant

    async def push_data_to_index(
        self,
        project,
        db_client
    ):

        settings = get_settings()

        batch_size = settings.INDEX_BATCH_SIZE

        chunk_model = ChunkModel(
            db_client=db_client
        )

        collection_name = self.create_collection_name(
            project["project_id"]
        )

        # Create collection once
        self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size
        )

        skip = 0

        while True:

            current_chunks = (
                await chunk_model.get_chunks_by_project_id(
                    project_id=project["project_id"],
                    skip=skip,
                    limit=batch_size
                )
            )

            # Stop when no more chunks exist
            if not current_chunks:
                break

            texts = [
                c["chunk_text"]
                for c in current_chunks
            ]

            metadata = [
                {
                    "project_id": project["project_id"],
                    "chunk_order": c["chunk_order"],
                    "chunk_length": c.get(
                        "chunk_length",
                        0
                    ),
                }

                for c in current_chunks
            ]

            # Generate embeddings asynchronously
            vectors = await asyncio.gather(*[

                asyncio.to_thread(
                    self.embedding_client.embed,
                    text,
                    "passage"
                )

                for text in texts
            ])

            # Upload current batch
            self.vectordb_client.add_documents(
                collection_name=collection_name,
                texts=texts,
                vectors=vectors,
                metadata=metadata
            )

            # Move to next batch
            skip += batch_size

        return True


    # Semantic Search

    def search_by_vector(
        self,
        project,
        text: str,
        top_k: int = 5
    ):

        collection_name = self.create_collection_name(
            project["project_id"]
        )

        query_vector = self.embedding_client.embed(
            text=text,
            doc_type="query",
        )

        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            query_vector=query_vector,
            top_k=top_k,
        )

        if not results:
            return []

        return results


    # Build Prompt

    def build_rag_prompt(
        self,
        query: str,
        relevant_docs: list
    ):

        # Detect Arabic language
        is_arabic = any(
            '\u0600' <= char <= '\u06FF'
            for char in query
        )

        if is_arabic:

            self.template_parser.set_language(
                "ar"
            )

        else:

            self.template_parser.set_language(
                "en"
            )

        system_prompt = self.template_parser.get(
            "rag",
            "system_prompt"
        )

        footer_prompt = self.template_parser.get(
            "rag",
            "footer_template_prompt"
        )

        documents_prompt = "\n\n".join([

            self.template_parser.get(
                "rag",
                "document_prompt",
                {
                    "doc_id": index + 1,
                    "text": doc["text"],
                }
            )

            for index, doc in enumerate(
                relevant_docs
            )
        ])

        if is_arabic:

            query_label = "سؤال المستخدم"

        else:

            query_label = "User Question"

        full_prompt = "\n\n".join([

            documents_prompt,

            f"{query_label}:\n{query}",

            footer_prompt,
        ])

        return system_prompt, full_prompt


    # Generate RAG Answer

    def answer_rag_question(
        self,
        project,
        query: str,
        top_k: int = 5
    ):

        relevant_docs = self.search_by_vector(
            project=project,
            text=query,
            top_k=top_k,
        )

        # Detect Arabic language
        is_arabic = any(
            '\u0600' <= char <= '\u06FF'
            for char in query
        )

        if not relevant_docs:

            if is_arabic:

                return {
                    "answer": (
                        "مش لاقية المعلومة دي "
                        "في الوصفات المتوفرة يا ست الكل 💛"
                    ),
                    "documents": []
                }

            return {
                "answer": (
                    "I could not find this information "
                    "in the available recipes 💛"
                ),
                "documents": []
            }

        system_prompt, full_prompt = self.build_rag_prompt(
            query=query,
            relevant_docs=relevant_docs,
        )

        chat_history = [

            self.generation_client.construct_prompt(
                query=system_prompt,
                role="system",
            )
        ]

        answer = self.generation_client.generate_response(
            prompt=full_prompt,
            chat_history=chat_history,
        )

        # Clean answer
        answer = (
            answer
            .replace("\\n", " ")
            .replace("\n", " ")
            .strip()
        )

        # Clean full prompt
        full_prompt = (
            full_prompt
            .replace("\\n", " ")
            .replace("\n", " ")
            .strip()
        )

        # Clean chat history
        for message in chat_history:

            message["content"] = (
                message["content"]
                .replace("\\n", " ")
                .replace("\n", " ")
                .strip()
            )

        # Clean retrieved documents
        for doc in relevant_docs:

            doc["text"] = (
                doc["text"]
                .replace("\\n", " ")
                .replace("\n", " ")
                .strip()
            )

        return {
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": chat_history,
            "documents": relevant_docs,
        }


    # Reset Collection

    def reset_vector_db_collection(
        self,
        project_id: str
    ):

        collection_name = self.create_collection_name(
            project_id
        )

        return self.vectordb_client.delete_collection(
            collection_name
        )


    # Collection Info

    def get_vector_db_collection_info(
        self,
        project_id: str
    ):

        collection_name = self.create_collection_name(
            project_id
        )

        return self.vectordb_client.is_collection_exists(
            collection_name
        )