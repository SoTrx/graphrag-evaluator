"""Tests for custom evaluators.

This file shows how to test your custom evaluators.
Run with: pytest test_evaluators.py
"""

from unittest.mock import Mock

import pytest
from config import EvaluationConfig
from evaluators.abstract_evaluator import AbstractEvaluator
from evaluators.custom_metrics_evaluator import CustomMetricsEvaluator
from pipeline import EvaluationPipeline


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    config = Mock(spec=EvaluationConfig)
    config.threshold = 3
    config.azure_endpoint = "https://test.endpoint"
    config.api_key = "test_key"
    config.azure_deployment = "test_deployment"
    config.api_version = "2024-01-01"
    return config


@pytest.mark.asyncio
async def test_custom_metrics_evaluator_initialization(mock_config):
    """Test that CustomMetricsEvaluator initializes correctly."""
    evaluator = CustomMetricsEvaluator(mock_config)

    assert evaluator.name == "CustomMetricsEvaluator"
    assert evaluator.config == mock_config
    assert evaluator.min_length == 100
    assert evaluator.max_length == 5000


@pytest.mark.asyncio
async def test_custom_metrics_evaluator_short_text(mock_config):
    """Test evaluation of short text."""
    evaluator = CustomMetricsEvaluator(mock_config)

    query = "Test query"
    context = "This is a short text."

    result = await evaluator.evaluate(query, context)

    # Check structure
    assert "word_count" in result
    assert "character_count" in result
    assert "length_check" in result
    assert "content_check" in result

    # Check values
    assert result["word_count"]["score"] == 5
    assert result["character_count"]["score"] == 22
    assert result["length_check"]["score"] == 0  # Too short
    assert result["content_check"]["score"] == 0  # Less than 10 words


@pytest.mark.asyncio
async def test_custom_metrics_evaluator_good_text(mock_config):
    """Test evaluation of well-sized text."""
    evaluator = CustomMetricsEvaluator(mock_config)

    query = "Test query"
    # Create text with good length
    context = " ".join(["word"] * 150)  # 150 words

    result = await evaluator.evaluate(query, context)

    # Check that length is acceptable
    assert result["word_count"]["score"] == 150
    assert result["length_check"]["score"] == 1  # Within range
    assert result["content_check"]["score"] == 1  # More than 10 words


@pytest.mark.asyncio
async def test_pipeline_with_multiple_evaluators(mock_config):
    """Test pipeline with multiple evaluators."""
    # Create evaluators
    evaluators = [
        CustomMetricsEvaluator(mock_config),
    ]

    # Create pipeline
    pipeline = EvaluationPipeline(evaluators)

    # Check pipeline setup
    assert len(pipeline) == 1
    assert "CustomMetricsEvaluator" in pipeline.get_evaluator_names()

    # Run evaluation
    query = "Test"
    context = "This is a test with enough words to pass the content check."
    result = await pipeline.run(query, context, "Test")

    # Check results
    assert "CustomMetricsEvaluator" in result
    assert "word_count" in result["CustomMetricsEvaluator"]


def test_pipeline_add_remove_evaluators(mock_config):
    """Test adding and removing evaluators from pipeline."""
    # Start with one evaluator
    evaluator1 = CustomMetricsEvaluator(mock_config)
    pipeline = EvaluationPipeline([evaluator1])

    assert len(pipeline) == 1

    # Add another evaluator
    evaluator2 = CustomMetricsEvaluator(mock_config)
    pipeline.add_evaluator(evaluator2)

    assert len(pipeline) == 2

    # Remove by name
    removed = pipeline.remove_evaluator("CustomMetricsEvaluator")

    assert removed is True
    assert len(pipeline) == 1

    # Try to remove non-existent evaluator
    removed = pipeline.remove_evaluator("NonExistent")
    assert removed is False


@pytest.mark.asyncio
async def test_evaluator_error_handling(mock_config):
    """Test that pipeline handles evaluator errors gracefully."""
    # Create a faulty evaluator
    class FaultyEvaluator(AbstractEvaluator):
        def _initialize(self):
            pass

        async def evaluate(self, query, context):
            raise ValueError("Intentional error for testing")

        @property
        def name(self):
            return "FaultyEvaluator"

    # Create pipeline with faulty evaluator
    pipeline = EvaluationPipeline([FaultyEvaluator(mock_config)])

    # Run should not crash
    result = await pipeline.run("test", "test", "Test")

    # Check error was captured
    assert "FaultyEvaluator" in result
    assert "error" in result["FaultyEvaluator"]
    assert "Intentional error" in result["FaultyEvaluator"]["error"]


if __name__ == "__main__":
    # Run tests with: python -m pytest test_evaluators.py -v
    pytest.main([__file__, "-v"])
