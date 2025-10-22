import asyncio

# Import pipeline components
from dotenv import load_dotenv
from evaluators import CustomMetricsEvaluator, RetrievalEvaluatorWrapper
from graph_sdk import SearchType
from pipeline import EvaluationPipeline
from utils import console, initialize

load_dotenv()


async def main():
    console.print(
        "[bold cyan]🚀 Starting GraphRAG Evaluation Pipeline[/bold cyan]\n", style="bold"
    )

    # Initialize configuration and GraphRAG contexts
    console.print(
        "[yellow]⚙️  Loading configuration and initializing GraphRAG contexts...[/yellow]")
    config, graphrag_gpt5, graphrag_gpt4 = initialize()

    # Build evaluation pipeline
    console.print("[yellow]⚙️  Building evaluation pipeline...[/yellow]")
    evaluators = [
        RetrievalEvaluatorWrapper(config),
        CustomMetricsEvaluator(config),
    ]
    pipeline = EvaluationPipeline(evaluators)

    console.print(
        f"[green]✓ Pipeline created with {len(pipeline)} evaluator(s): {pipeline.get_evaluator_names()}[/green]"
    )
    console.print()

    # Query
    query = "Evalue la quantité de sel moyenne de Damien et donne des recommandations pour l'améliorer."
    console.print(f"[bold magenta]❓ Query: {query}[/bold magenta]")

    # Actual evaluation - GPT 5
    console.print("\n[bold green]🔍 Running GPT-5 Analysis...[/bold green]")
    context = await graphrag_gpt5.search(SearchType.LOCAL, query)
    console.print_context("GPT-5 Context Response", context.response, context)

    # Run pipeline on GPT-5 results
    await pipeline.run(query, context.response, "GPT-5")

    # Actual evaluation - GPT 4
    console.print("\n[bold green]🔍 Running GPT-4 Analysis...[/bold green]")
    context = await graphrag_gpt4.search(SearchType.LOCAL, query)
    console.print_context("GPT-4 Context Response", context.response, context)

    # Run pipeline on GPT-4 results
    await pipeline.run(query, context.response, "GPT-4")

    console.print("\n[bold cyan]✅ Evaluation Complete![/bold cyan]")


if __name__ == "__main__":
    asyncio.run(main())
