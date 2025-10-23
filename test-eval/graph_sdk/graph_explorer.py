from dataclasses import dataclass
from pathlib import Path

from config import AoaiConfig
from graphrag.query.structured_search.base import SearchResult

from .graph_context import GraphContext
from .search_builder import Drift, Global, Local, SearchType


@dataclass
class GraphExplorer:

    def __init__(self,
                 azure_openai_config: AoaiConfig,
                 graph_path: Path) -> None:

        self._graph_context = GraphContext(graph_path=graph_path,
                                           aoai_config=azure_openai_config)
        self._local = Local.build(self._graph_context)
        self._global = Global.build(self._graph_context)
        self._drift = Drift.build(self._graph_context)

    async def search(self, query: str, type: SearchType = SearchType.LOCAL) -> SearchResult:
        match type:
            case SearchType.LOCAL:
                return await self._local.search(query)
            case SearchType.GLOBAL:
                return await self._global.search(query)
            case SearchType.DRIFT:
                return await self._drift.search(query)
