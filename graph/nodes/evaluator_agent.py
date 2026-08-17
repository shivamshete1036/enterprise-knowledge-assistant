import asyncio

from graph.state import GraphState
from evaluation.ragas_evaluator import RAGASEvaluator


evaluator = RAGASEvaluator()


def evaluator_agent(state: GraphState) -> GraphState:
    """
    Evaluate the generated RAG answer using RAGAS.
    """

    print("\n[Evaluator Agent] Starting...")

    question = state["question"]
    answer = state["answer"]

    retrieved_contexts = [
        document.page_content
        for document in state["retrieved_documents"]
    ]

    scores = asyncio.run(
        evaluator.evaluate(
            question=question,
            answer=answer,
            retrieved_contexts=retrieved_contexts,
        )
    )

    summary = evaluator.summarize(scores)

    print("[Evaluator Agent] Evaluation completed.")
    print(f"[Evaluator Agent] {summary}")

    return {
        **state,
        "evaluation_scores": scores,
        "evaluation_summary": summary,
    }