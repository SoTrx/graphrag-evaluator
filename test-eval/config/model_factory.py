from adapters.aoai_configs_adapter import aoai_configs_adapter
from app_config import settings
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from graphrag.config.enums import ModelType
from graphrag.config.models.language_model_config import LanguageModelConfig


class ModelFactory:
    def __init__(self) -> None:
        self.chat_models: dict[str,
                               LanguageModelConfig] = self.build_models(ModelType.AzureOpenAIChat)
        self.embedding_models: dict[str,
                                    LanguageModelConfig] = self.build_models(ModelType.AzureOpenAIEmbedding)

    def get(self, name: str, type: ModelType = ModelType.AzureOpenAIChat) -> LanguageModelConfig | None:
        match type:
            case ModelType.AzureOpenAIChat:
                return self.chat_models.get(name)
            case ModelType.AzureOpenAIEmbedding:
                return self.embedding_models.get(name)

    def get_simple_model(self, name: str, type: ModelType) -> AzureOpenAIModelConfiguration | None:
        match type:
            case ModelType.AzureOpenAIChat:
                model = self.chat_models.get(name)
            case ModelType.AzureOpenAIEmbedding:
                model = self.embedding_models.get(name)
            case _:
                model = None

        if model is None:
            return None

        return aoai_configs_adapter.to_azure_openai_model_config(model)

    def list_models(self, type: ModelType) -> list[str]:
        match type:
            case ModelType.AzureOpenAIChat:
                return list(self.chat_models.keys())
            case ModelType.AzureOpenAIEmbedding:
                return list(self.embedding_models.keys())
            case _:
                return []

    def build_models(self, model_type: ModelType) -> dict[str, LanguageModelConfig]:
        models: dict[str, LanguageModelConfig] = {}

        for model_name, model_config in settings.models[model_type].items():
            models[model_name] = LanguageModelConfig(
                api_base=model_config.api_base,
                api_key=model_config.api_key,
                deployment_name=model_config.deployment_name,
                model=model_config.model,
                api_version=model_config.api_version,
                type=model_type)
        return models
