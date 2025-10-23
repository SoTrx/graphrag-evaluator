from dataclasses import dataclass


@dataclass
class AoaiConfig:
    """Configuration for Azure OpenAI."""
    azure_endpoint: str
    api_key: str
    chat_deployment: str
    api_version: str
    embedding_deployment: str
    embedding_api_version: str
