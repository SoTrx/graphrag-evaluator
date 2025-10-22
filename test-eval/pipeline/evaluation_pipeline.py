"""Evaluation pipeline engine."""
from typing import Any, Dict, List, Optional, Sequence

from evaluators import AbstractEvaluator
from utils import console


class EvaluationPipeline:
    """Pipeline engine for running multiple evaluators."""

    def __init__(self, evaluators: Sequence[AbstractEvaluator]):
        """Initialize the pipeline with a stack of evaluators.

        Args:
            evaluators: List of evaluator instances to run in the pipeline
            console: Optional PrettyConsole for output formatting
        """
        self.evaluators = list(evaluators)

    async def run(
        self,
        query: str,
        context: Any,
        title: str = "Evaluation"
    ) -> Dict[str, Dict[str, Any]]:
        """Run all evaluators in the pipeline.

        Args:
            query: The query string to evaluate
            context: The context information to evaluate against
            title: Title prefix for display purposes

        Returns:
            Dictionary mapping evaluator names to their results
        """
        results = {}

        console.print(
            f"\n[bold cyan]🔬 Running {len(self.evaluators)} evaluator(s) for: {title}[/bold cyan]"
        )

        for evaluator in self.evaluators:
            console.print(
                f"[yellow]  ⚡ Running {evaluator.name}...[/yellow]"
            )

            try:
                result = await evaluator.evaluate(query, context)
                results[evaluator.name] = result

                # Pretty print the result
                console.print_evaluation_result(
                    f"{title} - {evaluator.name}",
                    result
                )
            except Exception as e:
                console.print(
                    f"[red]  ❌ Error in {evaluator.name}: {str(e)}[/red]"
                )
                results[evaluator.name] = {"error": str(e)}

        return results

    def add_evaluator(self, evaluator: AbstractEvaluator) -> None:
        """Add an evaluator to the pipeline.

        Args:
            evaluator: The evaluator to add
        """
        self.evaluators.append(evaluator)

    def remove_evaluator(self, evaluator_name: str) -> bool:
        """Remove an evaluator from the pipeline by name.

        Args:
            evaluator_name: Name of the evaluator to remove

        Returns:
            True if evaluator was removed, False if not found
        """
        for i, evaluator in enumerate(self.evaluators):
            if evaluator.name == evaluator_name:
                self.evaluators.pop(i)
                return True
        return False

    def get_evaluator_names(self) -> List[str]:
        """Get list of all evaluator names in the pipeline.

        Returns:
            List of evaluator names
        """
        return [evaluator.name for evaluator in self.evaluators]

    def __len__(self) -> int:
        """Return the number of evaluators in the pipeline."""
        return len(self.evaluators)

    def __repr__(self) -> str:
        """String representation of the pipeline."""
        evaluator_names = ", ".join(self.get_evaluator_names())
        return f"EvaluationPipeline(evaluators=[{evaluator_names}])"
