from utils.json_utils import load_jsonl_queries


def load_queries(asset_path: str = "assets/data.jsonl") -> list[str] | None:
    """Load queries from the JSONL data file.

    Returns:
        List of query strings if file exists and is valid, None otherwise
    """
    queries = load_jsonl_queries(asset_path)
    return queries
