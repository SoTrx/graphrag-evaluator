from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP
from graphrag.config.enums import ModelType
from graphrag.config.models.language_model_config import LanguageModelConfig

from graph_sdk import GraphExplorer

load_dotenv()

mcp = FastMCP("GraphRAG MCP Server")
graph: GraphExplorer


@mcp.tool
async def search(query: str) -> str:
    result = await graph.search(query)
    return str(result.response)


def main():
    # In reality, both the URL AND the API key must be set.
    # But starting with graphrag 3.0, the API key should also be picked up from other sources (e.g., Managed Identity).
    # So we only assert the URL here.
    chat_api_base = getenv("CHAT_DEPLOYMENT_URL", None)
    embedding_api_base = getenv("EMBEDDING_DEPLOYMENT_URL", None)
    assert chat_api_base is not None, "CHAT_DEPLOYMENT_URL environment variable is not set."
    assert embedding_api_base is not None, "EMBEDDING_DEPLOYMENT_URL environment variable is not set."

    chat_model = LanguageModelConfig(
        # Note : To be replaced by type chat for Graphrag 3.0+
        type=ModelType.AzureOpenAIChat,
        model=getenv("CHAT_MODEL_NAME", "gpt-5-chat"),
        deployment_name=getenv("CHAT_DEPLOYMENT_NAME", "gpt-5.0"),
        api_version=getenv("CHAT_API_VERSION", "2025-01-01-preview"),
        api_base=chat_api_base,
        api_key=getenv("CHAT_API_KEY", None)
    )

    df_embed_model = "text-embedding-3-small"
    embedding_model = LanguageModelConfig(
        # Note : To be replaced by type embedding for Graphrag 3.0+
        type=ModelType.AzureOpenAIEmbedding,
        model=getenv("EMBEDDING_MODEL_NAME", df_embed_model),
        deployment_name=getenv("EMBEDDING_DEPLOYMENT_NAME", df_embed_model),
        api_version=getenv("EMBEDDING_API_VERSION", "2025-01-01-preview"),
        api_base=embedding_api_base,
        api_key=getenv("EMBEDDING_API_KEY", None)
    )

    global graph
    graph = GraphExplorer(
        graph_path=Path("./graph/output"),
        chat_config=chat_model,
        embedding_config=embedding_model
    )

    mcp.run(transport="http", port=8000)


if __name__ == "__main__":
    main()
