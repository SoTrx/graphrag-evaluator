"""JSON utilities for loading and parsing data files."""
import json
from pathlib import Path


def load_jsonl_queries(file_path: str | Path) -> list[str] | None:
    """Load queries from a JSONL file.

    Each line in the JSONL file should be a JSON object with a "query" field.

    Args:
        file_path: Path to the JSONL file

    Returns:
        List of query strings if file exists and is valid, None otherwise

    Examples:
        >>> queries = load_jsonl_queries("assets/data.jsonl")
        >>> if queries:
        ...     for query in queries:
        ...         print(query)
    """
    queries = None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                queries = []
                for line in lines:
                    data = json.loads(line)
                    queries.append(data["query"])
    except FileNotFoundError:
        # File doesn't exist, queries remains None
        pass
    except (json.JSONDecodeError, KeyError):
        # Invalid JSON or missing "query" key, queries remains None
        pass

    return queries
