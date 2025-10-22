"""Retrieval evaluator implementation."""
from typing import Any, Dict

from azure.ai.evaluation import RetrievalEvaluator

from evaluators.abstract_evaluator import AbstractEvaluator


class RetrievalEvaluatorWrapper(AbstractEvaluator):
    """Wrapper for Azure AI RetrievalEvaluator."""

    def _initialize(self) -> None:
        """Initialize the Azure RetrievalEvaluator."""
        model_config = self.config.get_model_config()
        self.evaluator = RetrievalEvaluator(
            model_config=model_config,
            threshold=self.config.threshold
        )

    async def evaluate(self, query: str, context: Any) -> Dict[str, Any]:
        """Evaluate using Azure RetrievalEvaluator.

        Args:
            query: The query string to evaluate
            context: The context information from the search

        Returns:
            Dictionary containing retrieval evaluation metrics
        """
        # Convert context to string if needed
        context_str = str(context) if not isinstance(context, str) else context

        # Call the evaluator (it's synchronous)
        result = self.evaluator(query=query, context=context_str)

        return result

    @property
    def name(self) -> str:
        """Return the name of the evaluator."""
        return "RetrievalEvaluator"
