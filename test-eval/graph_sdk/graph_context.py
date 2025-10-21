from pathlib import Path
from typing import List

from graphrag.config.enums import ModelType
from graphrag.config.models.language_model_config import LanguageModelConfig
from graphrag.config.models.vector_store_schema_config import VectorStoreSchemaConfig
from graphrag.data_model.community import Community
from graphrag.data_model.community_report import CommunityReport
from graphrag.data_model.covariate import Covariate
from graphrag.data_model.entity import Entity
from graphrag.data_model.relationship import Relationship
from graphrag.data_model.text_unit import TextUnit
from graphrag.language_model.manager import ModelManager
from graphrag.language_model.protocol.base import ChatModel, EmbeddingModel
from graphrag.query.indexer_adapters import (
    read_indexer_communities,
    read_indexer_entities,
    read_indexer_relationships,
    read_indexer_report_embeddings,
    read_indexer_reports,
    read_indexer_text_units,
)
from graphrag.tokenizer.get_tokenizer import get_tokenizer
from graphrag.tokenizer.tokenizer import Tokenizer
from graphrag.vector_stores.lancedb import LanceDBVectorStore
from pandas import read_parquet


class GraphContext:
    """Base class for Graphrag search strategies."""

    entities: List[Entity]
    description_embedding_store: LanceDBVectorStore
    relationships: List[Relationship]
    community_reports: List[CommunityReport]
    full_content_reports: List[CommunityReport]
    communities: List[Community]
    text_units: List[TextUnit]
    covariates: List[Covariate]

    chat_model: ChatModel
    tokenizer: Tokenizer
    text_embedder: EmbeddingModel

    def __init__(self, graph_path: Path, aoia_endpoint: str, aoia_api_key: str) -> None:
        self.load_graph(graph_path)
        self.load_llm(aoia_endpoint, aoia_api_key)

    def load_graph(self, graph_path: Path) -> None:
        """Load a graph from the specified path."""
        LANCEDB_URI = f"{graph_path}/lancedb"
        COMMUNITY_REPORT_TABLE = "community_reports"
        ENTITY_TABLE = "entities"
        COMMUNITY_TABLE = "communities"
        RELATIONSHIP_TABLE = "relationships"
        COVARIATE_TABLE = "covariates"
        TEXT_UNIT_TABLE = "text_units"
        COMMUNITY_LEVEL = 2
        # Entities
        entity_df = read_parquet(f"{graph_path}/{ENTITY_TABLE}.parquet")
        community_df = read_parquet(f"{graph_path}/{COMMUNITY_TABLE}.parquet")
        report_df = read_parquet(
            f"{graph_path}/{COMMUNITY_REPORT_TABLE}.parquet")

        self.entities = read_indexer_entities(
            entity_df, community_df, COMMUNITY_LEVEL)

        # load description embeddings to an in-memory lancedb vectorstore
        # to connect to a remote db, specify url and port values.
        self.description_embedding_store = LanceDBVectorStore(
            vector_store_schema_config=VectorStoreSchemaConfig(
                index_name="default-entity-description"
            )
        )
        self.description_embedding_store.connect(db_uri=LANCEDB_URI)
        full_content_embedding_store = LanceDBVectorStore(
            vector_store_schema_config=VectorStoreSchemaConfig(
                index_name="default-community-full_content"
            )
        )
        full_content_embedding_store.connect(db_uri=LANCEDB_URI)

        self.full_content_reports = read_indexer_reports(
            report_df,
            community_df,
            COMMUNITY_LEVEL,
            content_embedding_col="full_content_embeddings",
        )
        read_indexer_report_embeddings(
            self.full_content_reports, full_content_embedding_store)

        # Relationships
        relationship_df = read_parquet(
            f"{graph_path}/{RELATIONSHIP_TABLE}.parquet")
        self.relationships = read_indexer_relationships(relationship_df)

        self.community_reports = read_indexer_reports(
            report_df, community_df, COMMUNITY_LEVEL)

        self.communities = read_indexer_communities(community_df, report_df)
        text_unit_df = read_parquet(f"{graph_path}/{TEXT_UNIT_TABLE}.parquet")
        self.text_units = read_indexer_text_units(text_unit_df)

    def load_llm(self, endpoint: str, api_key: str) -> None:
        chat_config = LanguageModelConfig(
            api_key=api_key,
            type=ModelType.AzureOpenAIChat,
            model="gpt-5-chat",
            deployment_name="gpt-5.0",
            api_base=endpoint,
            api_version="2025-01-01-preview",
            model_supports_json=True,
            max_retries=20,
        )
        self.chat_model = ModelManager().get_or_create_chat_model(
            name="local_search",
            model_type=ModelType.AzureOpenAIChat,
            config=chat_config,
        )

        embedding_config = LanguageModelConfig(
            api_key=api_key,
            type=ModelType.AzureOpenAIEmbedding,
            model="text-embedding-3-large",
            deployment_name="text-embedding-3-large",
            api_base=endpoint,
            api_version="2024-12-01-preview",
            max_retries=20,
        )

        self.text_embedder = ModelManager().get_or_create_embedding_model(
            name="local_search_embedding",
            model_type=ModelType.AzureOpenAIEmbedding,
            config=embedding_config,
        )

        self.tokenizer = get_tokenizer(chat_config)
