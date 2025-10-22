"""Abstract base class for evaluators."""
from abc import ABC, abstractmethod
from typing import Any, Dict

from utils import EvaluationConfig


class AbstractEvaluator(ABC):
    """Abstract base class for all evaluators in the pipeline."""

    def __init__(self, config: EvaluationConfig):
        """Initialize the evaluator with configuration.

        Args:
            config: The evaluation configuration
        """
        self.config = config
        self._initialize()

    @abstractmethod
    def _initialize(self) -> None:
        """Initialize the evaluator with specific setup.

        This method should be implemented by subclasses to perform
        any necessary initialization based on the config.
        """
        pass

    @abstractmethod
    async def evaluate(self, query: str, context: Any) -> Dict[str, Any]:
        """Evaluate the given query and context.

        Args:
            query: The query string to evaluate
            context: The context information (could be search results, etc.)

        Returns:
            Dictionary containing evaluation results with metrics
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the evaluator.

        Returns:
            String name of the evaluator
        """
        pass

    def __repr__(self) -> str:
        """String representation of the evaluator."""
        return f"{self.__class__.__name__}(name={self.name})"
