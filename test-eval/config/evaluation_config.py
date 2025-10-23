"""Configuration management for the evaluation pipeline."""
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from azure.ai.evaluation import AzureOpenAIModelConfiguration
from utils.env_utils import load_or_die

from . import AoaiConfig


class EvaluationConfig:
    """Configuration for evaluation pipeline."""

    # Azure OpenAI Configuration
    aoai_config: AoaiConfig

    # GraphRAG Configuration
    gpt_graph_path: Path

    # Evaluation Settings
    threshold: int = 3

    def __init__(self,
                 chat_deployment_env_name: str = "CHAT_DEPLOYMENT_NAME",
                 chat_model_env_name: str = "CHAT_MODEL_NAME",
                 embedding_deployment_env_name: str = "EMBEDDING_DEPLOYMENT_NAME",
                 graph_path: str = "GRAPH_PATH") -> None:

        self.aoai_config = AoaiConfig(
            azure_endpoint=load_or_die("AZURE_ENDPOINT"),
            api_key=load_or_die("AZURE_API_KEY"),
            chat_deployment_name=load_or_die(chat_deployment_env_name),
            chat_model_name=load_or_die(chat_model_env_name),
            api_version=load_or_die("AZURE_API_VERSION"),
            embedding_deployment=load_or_die(
                embedding_deployment_env_name),
            embedding_api_version=load_or_die(
                "AZURE_EMBEDDING_API_VERSION")
        )
        self.gpt_graph_path = Path(load_or_die(graph_path))

    def get_model_config(self) -> AzureOpenAIModelConfiguration:
        """Get Azure OpenAI model configuration.

        Returns:
            AzureOpenAIModelConfiguration instance
        """
        return AzureOpenAIModelConfiguration(
            azure_endpoint=self.aoai_config.azure_endpoint,
            api_key=self.aoai_config.api_key,
            azure_deployment=self.aoai_config.chat_deployment_name,
            api_version=self.aoai_config.api_version,
        )
