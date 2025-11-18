from utils.json_utils import load_jsonl_queries
from utils.pretty_print import console


def load_queries(asset_path: str = "assets/data.jsonl") -> list[str]:
    """Load queries from the JSONL data file.

    Returns:
        List of query strings if file exists and is valid, None otherwise
    """

    queries = load_jsonl_queries(asset_path)

    if not queries:
        console.print(
            "[bold red]✗ No query found in data file. Exiting Program[/bold red]")
        raise ValueError("No queries found")

    console.print(
        "[bold green]✓ Configuration and GraphRAG contexts initialized.[/bold green]")
    console.print("[bold magenta]❓ Queries : [/bold magenta]", queries)

    return queries
