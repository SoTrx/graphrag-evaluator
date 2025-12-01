from enum import Enum


class SearchType(Enum):
    """Enumeration of available search strategies."""
    LOCAL = "local"
    GLOBAL = "global"
    DRIFT = "drift"
