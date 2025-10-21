from graphrag.query.structured_search.base import SearchResult

from .graph_context import GraphContext
from .search_builder import Drift, Global, Local, SearchType


class GraphExplorer:

    def __init__(self, graph_context: GraphContext) -> None:
        self._local = Local.build(graph_context)
        self._global = Global.build(graph_context)
        self._drift = Drift.build(graph_context)

    async def search(self, type: SearchType, query: str) -> SearchResult:
        match type:
            case SearchType.LOCAL:
                return await self._local.search(query)
            case SearchType.GLOBAL:
                return await self._global.search(query)
            case SearchType.DRIFT:
                return await self._drift.search(query)
