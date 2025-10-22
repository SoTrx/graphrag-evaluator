"""Example: How to create a custom evaluator.

This file demonstrates how to create your own custom evaluator
by extending the AbstractEvaluator class.
"""

from typing import Any, Dict

from config import initialize
from evaluators.abstract_evaluator import AbstractEvaluator
from pipeline import EvaluationPipeline


class SentimentEvaluator(AbstractEvaluator):
    """Example: Simple sentiment analysis evaluator.

    This is a simplified example. In production, you would use
    a real sentiment analysis model or API.
    """

    def _initialize(self) -> None:
        """Initialize the sentiment evaluator.

        You can access self.config here to get configuration values.
        """
        # Example: Define sentiment keywords
        self.positive_words = {"good", "great",
                               "excellent", "amazing", "wonderful"}
        self.negative_words = {"bad", "terrible",
                               "awful", "poor", "disappointing"}

    async def evaluate(self, query: str, context: Any) -> Dict[str, Any]:
        """Evaluate sentiment in the context.

        Args:
            query: The original query (not used in this example)
            context: The context to analyze for sentiment

        Returns:
            Dictionary with sentiment metrics
        """
        # Convert context to lowercase string for analysis
        text = str(context).lower()
        words = set(text.split())

        # Count positive and negative words
        positive_count = len(words & self.positive_words)
        negative_count = len(words & self.negative_words)

        # Calculate sentiment score (-1 to 1)
        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0
            sentiment_label = "neutral"
        else:
            sentiment_score = (positive_count - negative_count) / total
            if sentiment_score > 0.3:
                sentiment_label = "positive"
            elif sentiment_score < -0.3:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"

        return {
            "sentiment_score": {
                "score": round(sentiment_score, 2),
                "reason": f"Sentiment is {sentiment_label} based on keyword analysis"
            },
            "positive_words": {
                "score": positive_count,
                "reason": f"Found {positive_count} positive words"
            },
            "negative_words": {
                "score": negative_count,
                "reason": f"Found {negative_count} negative words"
            }
        }

    @property
    def name(self) -> str:
        """Return the evaluator name."""
        return "SentimentEvaluator"


class LengthQualityEvaluator(AbstractEvaluator):
    """Example: Evaluates response length and quality metrics."""

    def _initialize(self) -> None:
        """Initialize with quality thresholds."""
        # Access configuration
        self.min_words = 50
        self.max_words = 500
        self.min_sentences = 3

    async def evaluate(self, query: str, context: Any) -> Dict[str, Any]:
        """Evaluate length and structure quality.

        Args:
            query: The original query
            context: The context to evaluate

        Returns:
            Dictionary with quality metrics
        """
        text = str(context)

        # Basic metrics
        words = text.split()
        sentences = text.split('.')

        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_word_per_sentence = word_count / max(sentence_count, 1)

        # Quality checks
        length_ok = self.min_words <= word_count <= self.max_words
        structure_ok = sentence_count >= self.min_sentences
        readable = 10 <= avg_word_per_sentence <= 25

        # Calculate overall quality score (0-10)
        quality_score = sum([
            3 if length_ok else 0,
            3 if structure_ok else 0,
            4 if readable else 0,
        ])

        return {
            "word_count": {
                "score": word_count,
                "reason": f"Response has {word_count} words (target: {self.min_words}-{self.max_words})"
            },
            "sentence_count": {
                "score": sentence_count,
                "reason": f"Response has {sentence_count} sentences (min: {self.min_sentences})"
            },
            "readability": {
                "score": round(avg_word_per_sentence, 1),
                "reason": f"Average {avg_word_per_sentence:.1f} words per sentence"
            },
            "overall_quality": {
                "score": quality_score,
                "reason": f"Quality score: {quality_score}/10"
            }
        }

    @property
    def name(self) -> str:
        """Return the evaluator name."""
        return "LengthQualityEvaluator"


# Example usage
async def example_usage():
    """Demonstrate how to use custom evaluators in a pipeline."""
    from utils import PrettyConsole

    # Initialize configuration
    config = initialize()
    console = PrettyConsole()

    # Create custom evaluators
    evaluators = [
        SentimentEvaluator(config),
        LengthQualityEvaluator(config),
    ]

    # Build pipeline
    pipeline = EvaluationPipeline(evaluators, console)

    # Example evaluation
    query = "What is the sentiment of this text?"
    context = """
    This is a great example of how to use custom evaluators.
    The implementation is excellent and very easy to understand.
    You can create amazing evaluators for your specific needs.
    """

    # Run evaluation
    results = await pipeline.run(query, context, "Custom Evaluation Example")

    return results


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
