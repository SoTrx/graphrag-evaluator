"""JSON utilities for loading and parsing data files."""
import json
from pathlib import Path


class DatasetEntry:
    """Represents a single entry in the dataset with query and ground truth."""

    def __init__(self, query: str, ground_truth: str):
        """Initialize a dataset entry.

        Args:
            query: The query string
            ground_truth: The ground truth answer
        """
        self.query = query
        self.ground_truth = ground_truth

    def __repr__(self) -> str:
        return f"DatasetEntry(query='{self.query}', ground_truth='{self.ground_truth}')"


def load_jsonl_queries(file_path: str | Path) -> list[DatasetEntry] | None:
    """Load queries and ground truths from a JSONL file.

    Each line in the JSONL file should be a JSON object with "query" and "ground_truth" fields.

    Args:
        file_path: Path to the JSONL file

    Returns:
        List of DatasetEntry objects if file exists and is valid, None otherwise

    Examples:
        >>> entries = load_jsonl_queries("assets/data.jsonl")
        >>> if entries:
        ...     for entry in entries:
        ...         print(entry.query, entry.ground_truth)
    """
    entries = None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                entries = []
                for line in lines:
                    data = json.loads(line)
                    entries.append(DatasetEntry(
                        query=data["query"],
                        ground_truth=data["ground_truth"]
                    ))
    except FileNotFoundError:
        # File doesn't exist, entries remains None
        pass
    except (json.JSONDecodeError, KeyError):
        # Invalid JSON or missing required keys, entries remains None
        pass

    return entries
