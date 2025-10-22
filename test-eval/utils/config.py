"""Configuration management for the evaluation pipeline."""
from dataclasses import dataclass
from pathlib import Path

from azure.ai.evaluation import AzureOpenAIModelConfiguration
from graph_sdk import GraphContext, GraphExplorer

from utils.env_utils import load_or_die


@dataclass
class EvaluationConfig:
    """Configuration for evaluation pipeline."""

    # Azure OpenAI Configuration
    azure_endpoint: str
    api_key: str
    azure_deployment: str
    api_version: str

    # GraphRAG Configuration
    gpt5_graph_path: Path
    gpt4_graph_path: Path

    # Evaluation Settings
    threshold: int = 3

    @classmethod
    def from_env(cls) -> "EvaluationConfig":
        """Create configuration from environment variables.

        Args:
            load_or_die_func: Function to load environment variables

        Returns:
            EvaluationConfig instance
        """
        return cls(
            azure_endpoint=load_or_die("AZURE_ENDPOINT"),
            api_key=load_or_die("AZURE_API_KEY"),
            azure_deployment=load_or_die("AZURE_DEPLOYMENT_NAME"),
            api_version=load_or_die("AZURE_API_VERSION"),
            gpt5_graph_path=Path("sample-gpt5/output"),
            gpt4_graph_path=Path("sample-gpt4/output"),
        )

    def get_model_config(self) -> AzureOpenAIModelConfiguration:
        """Get Azure OpenAI model configuration.

        Returns:
            AzureOpenAIModelConfiguration instance
        """
        return AzureOpenAIModelConfiguration(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            azure_deployment=self.azure_deployment,
            api_version=self.api_version,
        )

    def prepare_graph_rag_contexts(self) -> tuple[GraphExplorer, GraphExplorer]:
        """Prepare GraphRAG contexts for GPT-5 and GPT-4.

        Returns:
            Tuple of (graphrag_gpt5, graphrag_gpt4)
        """
        # Initialize GPT-5 GraphRAG context
        gpt5_ctx = GraphContext(
            graph_path=self.gpt5_graph_path,
            aoia_endpoint=self.azure_endpoint,
            aoia_api_key=self.api_key,
        )
        graphrag_gpt5 = GraphExplorer(gpt5_ctx)

        # Initialize GPT-4 GraphRAG context
        gpt4_ctx = GraphContext(
            graph_path=self.gpt4_graph_path,
            aoia_endpoint=self.azure_endpoint,
            aoia_api_key=self.api_key,
        )
        graphrag_gpt4 = GraphExplorer(gpt4_ctx)

        return graphrag_gpt5, graphrag_gpt4


def initialize() -> tuple[EvaluationConfig, GraphExplorer, GraphExplorer]:
    """Initialize and return the evaluation configuration and GraphRAG explorers.

    Returns:
        Tuple of (EvaluationConfig, graphrag_gpt5, graphrag_gpt4)
    """
    config = EvaluationConfig.from_env()
    graphrag_gpt5, graphrag_gpt4 = config.prepare_graph_rag_contexts()

    return config, graphrag_gpt5, graphrag_gpt4
