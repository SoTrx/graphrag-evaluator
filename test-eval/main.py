import asyncio
from pathlib import Path
from time import sleep

from azure.ai.evaluation import AzureOpenAIModelConfiguration
from graphrag.config.enums import ModelType

from adapters.aoai_configs_adapter import aoai_configs_adapter
from app_config import settings
from evaluator_workflow import run_cloud_evaluators, run_evaluators
from graph_sdk import GraphExplorer, SearchType
from main_setup import initialize
from utils import console


async def query_graphrag(graph_explorer: GraphExplorer, queries: list[str], search_type: SearchType = SearchType.LOCAL):
    # Actual evaluation - GPT 5
    console.print(
        f"\n[bold green]🔍 Running {graph_explorer.model_deployment_name} Analysis...[/bold green]")
    for query in queries:
        console.print(
            f"\n[bold purple]❓ Querying : {query} ...[/bold purple]")

        search_result = await graph_explorer.search(query, search_type)
        console.print_context(f"{graph_explorer.model_deployment_name} Context Response",
                              search_result.response, search_result)


async def main():
    console.print(
        "[bold cyan]🚀 Starting GraphRAG Evaluation Pipeline[/bold cyan]\n", style="bold"
    )
    queries, model_factory, graph_explorers = initialize()

    aoai_config = model_factory.get_simple_model(
        "gpt5", ModelType.AzureOpenAIChat)

    if aoai_config is None:
        console.print(
            "[bold red]❌ Error: Could not retrieve model configuration.[/bold red]"
        )
        return

    for graph_explorer in graph_explorers:
        # Kept for better content visibility
        # await query_graphrag(graph_explorer, queries)
        dataset = Path("assets/generated_dataset.jsonl")
        with dataset.open("w") as f:
            for query in queries:
                console.print(
                    f"\n[bold purple]❓ Querying : {query} ...[/bold purple]")

                search_result = await graph_explorer.search(query, SearchType.LOCAL)
                console.print_context(f"{graph_explorer.model_deployment_name} Context Response",
                                      search_result.response, search_result)
                f.write(
                    f'{{"query": "{query}", "response": "{search_result.response}", "context_text": "{search_result.context_text}"}}\n'
                )

        # Actual evaluators being run
        run_evaluators(graph_explorer, aoai_config)

        # NOTE : The deployment used here MUST be deployed in the AI foundry project, and not in the linked openai resource
        # This restriction is due to how the Foundry project evaluation service authenticates and accesses deployed models.
        project_url = settings.project_defaults.api_base
        evaluation_deployment_name = settings.project_defaults.cloud_evaluation_deployment_name
        run_cloud_evaluators(dataset, project_url, evaluation_deployment_name)

if __name__ == "__main__":
    asyncio.run(main())
