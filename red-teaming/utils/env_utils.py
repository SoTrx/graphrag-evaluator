"""Environment utilities for loading and validating environment variables."""
from os import environ


def load_or_die(key: str) -> str:
    """Load an environment variable or die trying.

    Args:
        key: The environment variable key to load

    Returns:
        The value of the environment variable

    Raises:
        AssertionError: If the environment variable is not set
    """
    value = environ.get(key)
    assert value is not None, f"{key} environment variable is not set."
    return value
