from typing import Final

from azure.ai.evaluation import AzureOpenAIModelConfiguration
from graphrag.config.enums import ModelType
from graphrag.config.models.language_model_config import LanguageModelConfig

from adapters.aoai_configs_adapter import aoai_configs_adapter
from app_config import settings


class ModelFactory:
    """Factory for creating and managing language model configurations."""

    MAX_RETRIES: Final[int] = 20
    chat_models: dict[str, LanguageModelConfig]
    embedding_models: dict[str, LanguageModelConfig]

    def __init__(self):
        self.chat_models = self._build_models(ModelType.AzureOpenAIChat)
        self.embedding_models = self._build_models(
            ModelType.AzureOpenAIEmbedding)

    def get(self, name: str, type: ModelType = ModelType.AzureOpenAIChat) -> LanguageModelConfig | None:
        """Get a language model configuration by name and type."""
        models = self._get_model_dict(type)
        return models.get(name) if models else None

    def get_simple_model(self, name: str, type: ModelType) -> AzureOpenAIModelConfiguration | None:
        """Get a simplified Azure OpenAI model configuration by name and type."""
        model = self.get(name, type)
        return aoai_configs_adapter.to_azure_openai_model_config(model) if model else None

    def list_models(self, type: ModelType) -> list[str]:
        """List all available model names for a given type."""
        models = self._get_model_dict(type)
        return list(models.keys()) if models else []

    def _get_model_dict(self, type: ModelType) -> dict[str, LanguageModelConfig] | None:
        """Get the appropriate model dictionary based on type."""
        match type:
            case ModelType.AzureOpenAIChat:
                return self.chat_models
            case ModelType.AzureOpenAIEmbedding:
                return self.embedding_models
            case _:
                return None

    def _build_models(self, model_type: ModelType) -> dict[str, LanguageModelConfig]:
        """Build language model configurations from settings."""
        models = {}
        for model_name, model_config in settings.models[model_type].items():
            models[model_name] = LanguageModelConfig(
                api_base=model_config.api_base,
                api_key=model_config.api_key,
                deployment_name=model_config.deployment_name,
                model=model_config.model,
                api_version=model_config.api_version,
                type=model_type,
                max_retries=self.MAX_RETRIES,
                model_supports_json=getattr(
                    model_config, 'model_supports_json', None),
            )
        return models
