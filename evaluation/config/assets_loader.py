from utils.json_utils import DatasetEntry, load_jsonl_queries
from utils.pretty_print import console


def load_queries(asset_path: str = "assets/data.jsonl") -> list[DatasetEntry]:
    """Load queries from the JSONL data file.

    Returns:
        List of DatasetEntry objects if file exists and is valid, None otherwise
    """

    entries = load_jsonl_queries(asset_path)

    if not entries:
        console.print(
            "[bold red]✗ No query found in data file. Exiting Program[/bold red]")
        raise ValueError("No queries found")

    console.print(
        "[bold green]✓ Configuration and GraphRAG contexts initialized.[/bold green]")
    console.print("[bold magenta]❓ Dataset Entries : [/bold magenta]", entries)

    return entries
