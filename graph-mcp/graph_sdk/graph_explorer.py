from pathlib import Path

from graphrag.config.models.language_model_config import LanguageModelConfig
from graphrag.query.structured_search.base import SearchResult

from .graph_context import GraphContext
from .search_builder import Drift, Global, Local, SearchType


class GraphExplorer:

    def __init__(self, graph_path: Path, chat_config: LanguageModelConfig, embedding_config: LanguageModelConfig) -> None:
        self._graph_context = GraphContext(graph_path=graph_path,
                                           chat_config=chat_config,
                                           embedding_config=embedding_config)
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
    
    @property
    def model_deployment_name(self) -> str | None:
        """Get the deployment name of the chat model."""
        return self._graph_context.chat_model.config.deployment_name
    
    @property
    def model_name(self) -> str | None:
        """Get the name of the chat model."""
        return self._graph_context.chat_model.config.model
