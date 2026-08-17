from openai import AsyncOpenAI

from utils.ragas_compat import setup_ragas_compatibility

# RAGAS 0.4.3 compatibility setup must happen
# before importing RAGAS.
setup_ragas_compatibility()

from ragas.embeddings import HuggingFaceEmbeddings
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy, Faithfulness


class RAGASEvaluator:
    """
    Evaluate RAG responses using RAGAS.

    Mandatory metrics:
    - Faithfulness
    - Answer Relevancy
    """

    def __init__(self):
        print("[RAGAS Evaluator] Initializing...")

        ollama_client = AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

        self.llm = llm_factory(
            "gpt-oss:120b-cloud",
            provider="openai",
            client=ollama_client,
        )

        self.embeddings = HuggingFaceEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            normalize_embeddings=True,
        )

        self.faithfulness = Faithfulness(
            llm=self.llm,
        )

        self.answer_relevancy = AnswerRelevancy(
            llm=self.llm,
            embeddings=self.embeddings,
        )

        print("[RAGAS Evaluator] Initialized successfully.")

    async def evaluate(
        self,
        question: str,
        answer: str,
        retrieved_contexts: list[str],
    ) -> dict:
        print("[RAGAS Evaluator] Evaluating response...")

        faithfulness_result = await self.faithfulness.ascore(
            user_input=question,
            response=answer,
            retrieved_contexts=retrieved_contexts,
        )

        relevancy_result = await self.answer_relevancy.ascore(
            user_input=question,
            response=answer,
        )

        scores = {
            "faithfulness": faithfulness_result.value,
            "answer_relevancy": relevancy_result.value,
        }

        print(
            "[RAGAS Evaluator] "
            f"Faithfulness: {scores['faithfulness']:.4f}"
        )

        print(
            "[RAGAS Evaluator] "
            f"Answer Relevancy: {scores['answer_relevancy']:.4f}"
        )

        return scores

    @staticmethod
    def summarize(scores: dict) -> str:
        faithfulness = scores.get("faithfulness", 0)
        relevancy = scores.get("answer_relevancy", 0)

        average = (faithfulness + relevancy) / 2

        if average >= 0.8:
            quality = "Good"
        elif average >= 0.6:
            quality = "Moderate"
        else:
            quality = "Needs improvement"

        return (
            f"Evaluation quality: {quality}. "
            f"Faithfulness={faithfulness:.2f}, "
            f"Answer Relevancy={relevancy:.2f}."
        )