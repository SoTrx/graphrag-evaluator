from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey
from graphrag.query.structured_search.local_search.mixed_context import (
    LocalSearchMixedContext,
)
from graphrag.query.structured_search.local_search.search import LocalSearch

from ..graph_context import GraphContext


class Local:
    """Graphrag Local Search strategy."""

    @staticmethod
    def build(ctx: GraphContext) -> LocalSearch:
        """Create and configure a LocalSearch instance."""
        context_builder = LocalSearchMixedContext(
            community_reports=ctx.community_reports,
            text_units=ctx.text_units,
            entities=ctx.entities,
            relationships=ctx.relationships,
            # if you did not run covariates during indexing, set this to None
            # covariates=covariates,
            entity_text_embeddings=ctx.description_embedding_store,
            # if the vectorstore uses entity title as ids, set this to EntityVectorStoreKey.TITLE
            embedding_vectorstore_key=EntityVectorStoreKey.ID,
            text_embedder=ctx.text_embedder,
            tokenizer=ctx.tokenizer,
        )
        local_context_params = {
            "text_unit_prop": 0.5,
            "community_prop": 0.1,
            "conversation_history_max_turns": 5,
            "conversation_history_user_turns_only": True,
            "top_k_mapped_entities": 10,
            "top_k_relationships": 10,
            "include_entity_rank": True,
            "include_relationship_weight": True,
            "include_community_rank": False,
            "return_candidate_context": False,
            # set this to EntityVectorStoreKey.TITLE if the vectorstore uses entity title as ids
            "embedding_vectorstore_key": EntityVectorStoreKey.ID,
            # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 5000)
            "max_tokens": 12_000,
        }

        model_params = {
            # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 1000=1500)
            "max_tokens": 2_000,
            "temperature": 0.0,
        }

        return LocalSearch(
            model=ctx.chat_model,
            context_builder=context_builder,
            tokenizer=ctx.tokenizer,
            model_params=model_params,
            context_builder_params=local_context_params,
            # free form text describing the response type and format, can be anything, e.g. prioritized list, single paragraph, multiple paragraphs, multiple-page report
            response_type="multiple paragraphs",
        )
