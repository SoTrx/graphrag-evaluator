
import asyncio
from os import environ
from pathlib import Path

from azure.ai.evaluation import AzureOpenAIModelConfiguration, RetrievalEvaluator
from dotenv import load_dotenv

from graph_sdk import GraphContext, GraphExplorer, SearchType

load_dotenv()


async def main():
    # Env
    endpoint = load_or_die("AZURE_ENDPOINT")
    api_key = load_or_die("AZURE_API_KEY")
    deployment_name = load_or_die("AZURE_DEPLOYMENT_NAME")
    api_version = load_or_die("AZURE_API_VERSION")

    # Rag integration
    gpt5_ctx = GraphContext(
        graph_path=Path("sample-gpt5/output"),
        aoia_endpoint=endpoint,
        aoia_api_key=api_key
    )
    graphrag = GraphExplorer(gpt5_ctx)
    # await search_and_print_results(graphrag)

    # Evaluation
    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=endpoint,
        api_key=api_key,
        azure_deployment=deployment_name,
        api_version=api_version,
    )
    evaluate = RetrievalEvaluator(model_config=model_config, threshold=3)

    # Actual evaluation
    query = "Who is scrooge ?"
    context = await graphrag.search(SearchType.LOCAL, query)
    result = evaluate(query=query, context=str(context.response))
    print(result)


async def search_and_print_results(explorer: GraphExplorer):
    """
    Search and print results from the graph explorer.
    """
    # Local
    result = await explorer.search(SearchType.LOCAL, "Who is scrooge?")
    print(result.response)

    # Global
    result = await explorer.search(SearchType.GLOBAL, "What are the main themes of the story?")
    print(result.response)

    # Drift
    result = await explorer.search(SearchType.DRIFT, "Who is scrooge?")
    print(result.response)


def load_or_die(key: str) -> str:
    """Load an environment variable or die trying."""
    value = environ.get(key)
    assert value is not None, f"{key} environment variable is not set."
    return value


if __name__ == "__main__":
    asyncio.run(main())
