"""Configuration module for GraphRAG evaluation."""
from pathlib import Path

from azure.ai.evaluation import AzureOpenAIModelConfiguration

from graph_sdk import GraphContext

from .env_utils import load_or_die
from .pretty_print import PrettyConsole


class EvaluationConfig:
    """Configuration class for GraphRAG evaluation setup."""

    def __init__(self):
        self.console = PrettyConsole()

    def initialize(self):
        """Initialize GraphRAG contexts and evaluation model configuration."""
        # Load environment variables
        endpoint = load_or_die("AZURE_ENDPOINT")
        api_key = load_or_die("AZURE_API_KEY")
        deployment_name = load_or_die("AZURE_DEPLOYMENT_NAME")
        api_version = load_or_die("AZURE_API_VERSION")

        # Initialize GraphRAG contexts
        self.console.print(
            "[yellow]⚙️  Initializing GraphRAG contexts...[/yellow]")
        gpt5_ctx = GraphContext(
            graph_path=Path("sample-gpt5/output"),
            aoia_endpoint=endpoint,
            aoia_api_key=api_key
        )

        gpt4_ctx = GraphContext(
            graph_path=Path("sample-gpt4/output"),
            aoia_endpoint=endpoint,
            aoia_api_key=api_key
        )

        # Setup evaluation model configuration
        self.console.print(
            "[yellow]⚙️  Setting up evaluation model...[/yellow]")
        model_config = AzureOpenAIModelConfiguration(
            azure_endpoint=endpoint,
            api_key=api_key,
            azure_deployment=deployment_name,
            api_version=api_version,
        )

        return gpt5_ctx, gpt4_ctx, model_config
