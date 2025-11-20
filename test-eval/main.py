import asyncio
import json
from functools import partial
from pathlib import Path
from typing import Dict

from graphrag.config.enums import ModelType

from evaluator_workflow import evaluate_cloud, evaluate_locally
from graph_sdk import GraphExplorer, SearchType
from main_setup import initialize
from utils import console
from utils.concurrency import limit_concurrency
from utils.json_utils import DatasetEntry

# Limit to 3 concurrent searches
search_limiter = asyncio.Semaphore(3)


async def main():
    console.print("[bold cyan]🚀 Starting Evaluation Pipeline[/bold cyan]\n")
    dataset_entries, factory, graph_explorers = initialize()

    aoai_config = factory.get_simple_model("gpt5", ModelType.AzureOpenAIChat)
    assert aoai_config is not None, "Failed to get Azure OpenAI model configuration."

    # For each GraphRAG implementation (sample-gpt4, sample-gpt5)...
    for graph_explorer in graph_explorers:
        rag_model = graph_explorer.model_deployment_name

        # Step 1 : Query the graph concurrently for all dataset entries
        graph_search = partial(__search, graph_explorer)
        responses = await asyncio.gather(*map(graph_search, dataset_entries))

        # Step 2 : Create the corresponding dataset
        dataset = Path(f"assets/generated_dataset_{rag_model}.jsonl")
        with dataset.open("w") as f:
            for entry in responses:
                f.write(f'{json.dumps(entry)}\n')

        # Step 3 : Evaluate the dataset locally or in cloud
        evaluation_result = evaluate_locally(dataset, aoai_config)

        # NOTE : Uncomment below to run cloud evaluators
        # project_url = settings.project_defaults.api_base
        # evaluation_deployment_name = settings.project_defaults.cloud_evaluation_deployment_name
        # run_cloud_evaluators(dataset, project_url, evaluation_deployment_name)

        console.print(evaluation_result)


@limit_concurrency(search_limiter)
async def __search(explorer: GraphExplorer, entry: DatasetEntry) -> Dict[str, str]:
    """
     Perform a search on the graph rag using the provided dataset entry.
     """
    console.print(f"[bold purple] Querying : {entry.query} ...[/bold purple]")
    search_result = await explorer.search(entry.query, SearchType.LOCAL)
    console.print(f"[green] Querying : {entry.query} ... OK ![/green]")

    return {
        "query": json.dumps(entry.query),
        "ground_truth": json.dumps(entry.ground_truth),
        "response": json.dumps(search_result.response),
        "context_text": json.dumps(search_result.context_text)
    }

if __name__ == "__main__":
    asyncio.run(main())
