"""Example custom evaluator implementation."""
from typing import Any, Dict

from evaluators.abstract_evaluator import AbstractEvaluator


class CustomMetricsEvaluator(AbstractEvaluator):
    """Example custom evaluator for demonstrating extensibility.

    This evaluator calculates custom metrics like response length,
    word count, etc. You can create similar evaluators for your
    specific needs.
    """

    def _initialize(self) -> None:
        """Initialize the custom evaluator.

        Add any setup needed for your custom evaluator here.
        """
        # Example: you could load models, set up connections, etc.
        self.min_length = 100
        self.max_length = 5000

    async def evaluate(self, query: str, context: Any) -> Dict[str, Any]:
        """Evaluate using custom metrics.

        Args:
            query: The query string to evaluate
            context: The context information from the search

        Returns:
            Dictionary containing custom evaluation metrics
        """
        context_str = str(context) if not isinstance(context, str) else context

        # Calculate custom metrics
        word_count = len(context_str.split())
        char_count = len(context_str)

        # Example quality checks
        length_ok = self.min_length <= char_count <= self.max_length
        has_content = word_count > 10

        # Return results in a structured format
        return {
            "word_count": {
                "score": word_count,
                "reason": f"Response contains {word_count} words"
            },
            "character_count": {
                "score": char_count,
                "reason": f"Response contains {char_count} characters"
            },
            "length_check": {
                "score": 1 if length_ok else 0,
                "reason": f"Length is {'within' if length_ok else 'outside'} acceptable range ({self.min_length}-{self.max_length})"
            },
            "content_check": {
                "score": 1 if has_content else 0,
                "reason": f"Response {'has' if has_content else 'lacks'} sufficient content"
            }
        }

    @property
    def name(self) -> str:
        """Return the name of the evaluator."""
        return "CustomMetricsEvaluator"
