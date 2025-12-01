from azure.ai.evaluation import AzureOpenAIModelConfiguration
from graphrag.config.enums import ModelType
from graphrag.config.models.language_model_config import LanguageModelConfig


class aoai_configs_adapter:
    @staticmethod
    def to_azure_openai_model_config(language_model_config: LanguageModelConfig) -> AzureOpenAIModelConfiguration:
        """
        Converts a LanguageModelConfig to AzureOpenAIModelConfiguration.

        Args:
            language_model_config: GraphRAG language model configuration

        Returns:
            AzureOpenAIModelConfiguration: Configuration compatible with Azure AI Evaluation

        Raises:
            ValueError: If a required property is None or missing
        """
        # Validate required fields
        if not language_model_config.api_base:
            raise ValueError(
                "azure_endpoint (api_base) is required but is None or empty")

        if not language_model_config.api_key:
            raise ValueError("api_key is required but is None or empty")

        if not language_model_config.deployment_name:
            raise ValueError(
                "azure_deployment (deployment_name) is required but is None or empty")

        if not language_model_config.api_version:
            raise ValueError("api_version is required but is None or empty")

        return AzureOpenAIModelConfiguration(
            azure_endpoint=language_model_config.api_base,
            api_key=language_model_config.api_key,
            azure_deployment=language_model_config.deployment_name,
            api_version=language_model_config.api_version
        )
