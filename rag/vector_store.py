import chromadb
from langchain_core.documents import Document

from rag.embeddings import EmbeddingModel


class VectorStore:
    """
    ChromaDB-based vector store for the enterprise knowledge base.
    """

    def __init__(
        self,
        persist_directory: str = "./data/chroma",
        collection_name: str = "enterprise_knowledge",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

        self.embedding_model = EmbeddingModel()

    def add_documents(self, documents: list[Document]) -> None:
        """
        Generate embeddings and store documents in ChromaDB.
        """

        if not documents:
            return

        texts = [document.page_content for document in documents]

        embeddings = self.embedding_model.embed_documents(texts)

        ids = [
            f"doc_{index}"
            for index in range(len(documents))
        ]

        metadatas = [
            document.metadata
            for document in documents
        ]

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict:
        """
        Search the vector store using semantic similarity.
        """

        query_embedding = self.embedding_model.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        return results

    def count(self) -> int:
        """
        Return the number of documents stored in ChromaDB.
        """

        return self.collection.count()