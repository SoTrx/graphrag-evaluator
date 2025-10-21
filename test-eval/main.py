
import asyncio
from os import environ
from pathlib import Path
from typing import Union

from azure.ai.evaluation import AzureOpenAIModelConfiguration, RetrievalEvaluator
from dotenv import load_dotenv
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from graph_sdk import GraphContext, GraphExplorer, SearchType

load_dotenv()

# Initialize rich console
console = Console()


def pretty_print_context(title: str, context_response: Union[str, dict, list], context_obj=None):
    """Pretty print context response with colors and formatting."""
    console.print()

    # Display the main response
    if isinstance(context_response, (dict, list)):
        # For structured data, show it as formatted JSON
        console.print(Panel(
            JSON.from_data(context_response),
            title=f"[bold green]📄 {title} - Response[/bold green]",
            border_style="blue",
            expand=False
        ))
    else:
        # For string responses, show as text
        console.print(Panel(
            Text(str(context_response), style="bright_blue"),
            title=f"[bold green]📄 {title} - Response[/bold green]",
            border_style="blue",
            expand=False
        ))

    # If we have the full context object, show additional details
    if context_obj is not None:
        console.print()

        # Create a table for context metadata
        metadata_table = Table(
            title=f"[bold cyan]📋 {title} - Context Metadata[/bold cyan]",
            show_header=True,
            header_style="bold magenta"
        )
        metadata_table.add_column("Property", style="yellow", justify="left")
        metadata_table.add_column(
            "Value", style="bright_green", justify="left")

        # Show available attributes of the context object
        for attr_name in dir(context_obj):
            if not attr_name.startswith('_'):  # Skip private attributes
                try:
                    attr_value = getattr(context_obj, attr_name)
                    if not callable(attr_value):  # Skip methods
                        # Truncate long values for display
                        str_value = str(attr_value)
                        if len(str_value) > 100:
                            str_value = str_value[:97] + "..."
                        metadata_table.add_row(attr_name, str_value)
                except Exception:
                    metadata_table.add_row(
                        attr_name, "[red]Error accessing value[/red]")

        console.print(metadata_table)


def pretty_print_evaluation_result(title: str, result: dict):
    """Pretty print evaluation result with colors and formatting."""
    console.print()

    # Create a table for the evaluation metrics
    table = Table(title=f"[bold cyan]📊 {title}[/bold cyan]",
                  show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="yellow", justify="left")
    table.add_column("Score", style="bright_green", justify="center")
    table.add_column("Reason", style="white", justify="left")

    # Add rows for each metric in the result
    for key, value in result.items():
        if isinstance(value, dict):
            score = value.get('score', 'N/A')
            reason = value.get('reason', 'No reason provided')
            table.add_row(key, str(score),
                          reason[:50] + "..." if len(reason) > 50 else reason)
        else:
            table.add_row(key, str(value), "")

    console.print(table)

    # Also show the full JSON for detailed inspection
    console.print()
    console.print(Panel(
        JSON.from_data(result),
        title="[bold yellow]📋 Detailed Result JSON[/bold yellow]",
        border_style="yellow",
        expand=False
    ))


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
    # await search_and_print_results(graphrag)

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
    pretty_print_context("GPT-5 Context Response", context.response, context)

    result = evaluate(query=query, context=str(context.response))
    pretty_print_evaluation_result("GPT-5 Evaluation Result", result)

    # Actual evaluation - GPT 4
    console.print("\n[bold green]🔍 Running GPT-4 Analysis...[/bold green]")
    context = await graphrag_gpt4.search(SearchType.LOCAL, query)
    pretty_print_context("GPT-4 Context Response", context.response, context)

    result = evaluate(query=query, context=str(context.response))
    pretty_print_evaluation_result("GPT-4 Evaluation Result", result)

    console.print("\n[bold cyan]✅ Evaluation Complete![/bold cyan]")


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
