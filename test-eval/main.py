
import asyncio

from azure.ai.evaluation import RetrievalEvaluator
from dotenv import load_dotenv

from graph_sdk import GraphExplorer, SearchType
from utils import EvaluationConfig, PrettyConsole

load_dotenv()

# Initialize pretty console
console = PrettyConsole()


async def main():
    console.print(
        "[bold cyan]🚀 Starting GraphRAG Evaluation[/bold cyan]", style="bold")
    console.print()

    # Initialize configuration
    config = EvaluationConfig()
    gpt5_ctx, gpt4_ctx, model_config = config.initialize()

    # Create explorers
    graphrag_gpt5 = GraphExplorer(gpt5_ctx)
    graphrag_gpt4 = GraphExplorer(gpt4_ctx)

    # Create evaluator
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
