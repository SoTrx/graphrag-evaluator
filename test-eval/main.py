import asyncio
from functools import partial

from azure.ai.evaluation import (
    EvaluatorConfig,
    GroundednessEvaluator,
    QAEvaluator,
    evaluate,
)
from config import EvaluationConfig, load_queries

# Import pipeline components
from dotenv import load_dotenv

# from evaluators import CustomMetricsEvaluator, RetrievalEvaluatorWrapper
from graph_sdk import GraphExplorer, SearchType

# from pipeline import EvaluationPipeline
from utils import console

load_dotenv()


async def main():
    console.print(
        "[bold cyan]🚀 Starting GraphRAG Evaluation Pipeline[/bold cyan]\n", style="bold"
    )

    # Initialize configuration and GraphRAG contexts
    console.print(
        "[yellow]⚙️  Loading configuration and initializing GraphRAG contexts...[/yellow]")

    queries = load_queries()
    aoai_config_gpt5 = EvaluationConfig(chat_deployment_env_name="CHAT_DEPLOYMENT_NAME",
                                        chat_model_env_name="CHAT_MODEL_NAME",
                                        embedding_deployment_env_name="EMBEDDING_DEPLOYMENT_NAME",
                                        graph_path="GRAPH5_PATH")
    aoai_config_gpt4 = EvaluationConfig(chat_deployment_env_name="CHAT_GPT4_1mini_DEPLOYMENT_NAME",
                                        chat_model_env_name="CHAT_GPT4_1mini_MODEL_NAME",
                                        embedding_deployment_env_name="EMBEDDING_DEPLOYMENT_NAME",
                                        graph_path="GRAPH4_PATH")

    graph5 = GraphExplorer(
        azure_openai_config=aoai_config_gpt5.aoai_config,
        graph_path=aoai_config_gpt5.gpt_graph_path
    )

    graph4 = GraphExplorer(
        azure_openai_config=aoai_config_gpt4.aoai_config,
        graph_path=aoai_config_gpt4.gpt_graph_path
    )

    groundedness_eval = GroundednessEvaluator(
        aoai_config_gpt5.get_model_config(), threshold=3)
    qa_eval = QAEvaluator(
        aoai_config_gpt5.get_model_config(), threshold=3)

    if not queries:
        console.print(
            "[bold red]✗ No query found in data file. Exiting Program[/bold red]")
        return

    query = queries[0]

    console.print(
        "[bold green]✓ Configuration and GraphRAG contexts initialized.[/bold green]\nLoaded query from data file : " + query)

    # Query
    console.print(f"[bold magenta]❓ Query: {query}[/bold magenta]")

    # Actual evaluation - GPT 5
    console.print("\n[bold green]🔍 Running GPT-5 Analysis...[/bold green]")
    search_result = await graph5.search(query, SearchType.LOCAL)
    console.print_context("GPT-5 Context Response",
                          search_result.response, search_result)

    # Actual evaluation - GPT 4
    console.print("\n[bold green]🔍 Running GPT-4 Analysis...[/bold green]")
    search_result = await graph4.search(query, SearchType.LOCAL)
    console.print_context("GPT-4 Context Response",
                          search_result.response, search_result)

    default_config: EvaluatorConfig = {
        "column_mapping": {
            "query": "${data.query}",
            "context": "${target.context_text}",
            "response": "${target.response}"
        }
    }

    evaluation_result = evaluate(
        data="assets/data.jsonl",
        target=graph5.search,
        evaluators={
            "groundedness": groundedness_eval,
            "qa": qa_eval,
        },
        evaluator_config={
            "default": default_config
        }
    )

    console.print(evaluation_result)

    console.print(
        "\n[bold purple]✅ Evaluation for GPT-5 Complete![/bold purple]")

    evaluation_result = evaluate(
        data="assets/data.jsonl",
        target=graph4.search,
        evaluators={
            "groundedness": groundedness_eval,
            "qa": qa_eval,
        },
        evaluator_config={
            "default": default_config
        }
    )

    console.print(evaluation_result)

    console.print(
        "\n[bold purple]✅ Evaluation for GPT-4.1-Mini Complete![/bold purple]")

if __name__ == "__main__":
    asyncio.run(main())
