from langchain_ollama import ChatOllama

from graph.state import GraphState


def response_agent(state: GraphState) -> GraphState:
    """
    Generate a grounded answer using the retrieved documents.
    """

    question = state["question"]
    documents = state["retrieved_documents"]

    print("\n[Response Agent] Starting...")

    if not documents:
        print("[Response Agent] No documents were retrieved.")

        return {
            **state,
            "answer": (
                "I could not find relevant information "
                "in the knowledge base."
            ),
        }

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not invent or assume information.
2. If the context does not contain enough information,
   say that the information is not available in the knowledge base.
3. Give a clear and concise answer.
4. Base the answer strictly on the retrieved context.

Retrieved Context:
{context}

User Question:
{question}

Answer:
"""

    llm = ChatOllama(
        model="gpt-oss:120b-cloud",
        temperature=0,
    )

    response = llm.invoke(prompt)

    answer = response.content

    print("[Response Agent] Answer generated.")

    return {
        **state,
        "answer": answer,
    }