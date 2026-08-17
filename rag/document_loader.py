from pathlib import Path

from langchain_core.documents import Document


def load_documents(knowledge_base_path: str) -> list[Document]:
    """
    Load all text documents from the knowledge base.
    """

    knowledge_base = Path(knowledge_base_path)

    documents = []

    for file_path in knowledge_base.rglob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        document = Document(
            page_content=text,
            metadata={
                "source": str(file_path)
            }
        )

        documents.append(document)

    return documents


if __name__ == "__main__":
    documents = load_documents("knowledge_base")

    print(f"Loaded documents: {len(documents)}")

    for document in documents:
        print("\n--- Document ---")
        print(document.page_content)
        print("Metadata:", document.metadata)