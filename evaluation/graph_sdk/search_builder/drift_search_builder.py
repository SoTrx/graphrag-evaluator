from graphrag.config.models.drift_search_config import DRIFTSearchConfig
from graphrag.query.structured_search.drift_search.drift_context import (
    DRIFTSearchContextBuilder,
)
from graphrag.query.structured_search.drift_search.search import DRIFTSearch

from ..graph_context import GraphContext


class Drift:
    """Graphrag DRIFT Search strategy."""

    @staticmethod
    def build(ctx: GraphContext) -> DRIFTSearch:
        """Create and configure a DRIFTSearch instance."""
        drift_params = DRIFTSearchConfig(
            primer_folds=1,
            drift_k_followups=3,
            n_depth=3,
        )

        context_builder = DRIFTSearchContextBuilder(
            model=ctx.chat_model,
            text_embedder=ctx.text_embedder,
            entities=ctx.entities,
            relationships=ctx.relationships,
            reports=ctx.full_content_reports,
            entity_text_embeddings=ctx.description_embedding_store,
            text_units=ctx.text_units,
            tokenizer=ctx.tokenizer,
            config=drift_params,
        )

        return DRIFTSearch(
            model=ctx.chat_model, context_builder=context_builder, tokenizer=ctx.tokenizer
        )
