
import asyncio
from pathlib import Path

from azure.ai.evaluation import AzureOpenAIModelConfiguration, RetrievalEvaluator
from dotenv import load_dotenv
from graph_sdk import GraphContext, GraphExplorer, SearchType
from utils import PrettyConsole, load_or_die

load_dotenv()

# Initialize pretty console
console = PrettyConsole()


async def main():
    console.print(
        "[bold cyan]🚀 Starting GraphRAG Evaluation[/bold cyan]", style="bold")
    console.print()

    # Env
    endpoint = load_or_die("AZURE_ENDPOINT")
    api_key = load_or_die("AZURE_API_KEY")
    deployment_name = load_or_die("AZURE_DEPLOYMENT_NAME")
    api_version = load_or_die("AZURE_API_VERSION")

    # Rag integration
    console.print("[yellow]⚙️  Initializing GraphRAG contexts...[/yellow]")
    gpt5_ctx = GraphContext(
        graph_path=Path("sample-gpt5/output"),
        aoia_endpoint=endpoint,
        aoia_api_key=api_key
    )
    graphrag_gpt5 = GraphExplorer(gpt5_ctx)

    # Rag integration
    gpt4_ctx = GraphContext(
        graph_path=Path("sample-gpt4/output"),
        aoia_endpoint=endpoint,
        aoia_api_key=api_key
    )
    graphrag_gpt4 = GraphExplorer(gpt4_ctx)

    # Example usage of GraphRagSearchService (commented out):
    # from services import GraphRagSearchService
    # search_service = GraphRagSearchService(graphrag_gpt5)
    # await search_service.search_and_print_results()

    # Evaluation
    console.print("[yellow]⚙️  Setting up evaluation model...[/yellow]")
    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=endpoint,
        api_key=api_key,
        azure_deployment=deployment_name,
        api_version=api_version,
    )
    evaluate = RetrievalEvaluator(model_config=model_config, threshold=3)

    # Query
    query = "Evalue la quantité de sel moyenne de Damien et donne des recommandations pour l'améliorer."
    console.print(f"[bold magenta]❓ Query: {query}[/bold magenta]")

    # Actual evaluation - GPT 5
    console.print("\n[bold green]🔍 Running GPT-5 Analysis...[/bold green]")
    context = await graphrag_gpt5.search(SearchType.LOCAL, query)
    console.print_context("GPT-5 Context Response", context.response, context)

    result = evaluate(query=query, context=str(context.response))
    console.print_evaluation_result("GPT-5 Evaluation Result", result)

    # Actual evaluation - GPT 4
    console.print("\n[bold green]🔍 Running GPT-4 Analysis...[/bold green]")
    context = await graphrag_gpt4.search(SearchType.LOCAL, query)
    console.print_context("GPT-4 Context Response", context.response, context)

    result = evaluate(query=query, context=str(context.response))
    console.print_evaluation_result("GPT-4 Evaluation Result", result)

    console.print("\n[bold cyan]✅ Evaluation Complete![/bold cyan]")


if __name__ == "__main__":
    asyncio.run(main())
