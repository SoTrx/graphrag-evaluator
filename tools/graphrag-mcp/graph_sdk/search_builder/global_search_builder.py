from graphrag.query.structured_search.global_search.community_context import (
    GlobalCommunityContext,
)
from graphrag.query.structured_search.global_search.search import GlobalSearch

from ..graph_context import GraphContext


class Global:
    """Graphrag Global Search strategy."""

    @staticmethod
    def build(ctx: GraphContext) -> GlobalSearch:
        """Create and configure a GlobalSearch instance."""
        context_builder = GlobalCommunityContext(
            community_reports=ctx.community_reports,
            communities=ctx.communities,
            # default to None if you don't want to use community weights for ranking
            entities=ctx.entities,
            tokenizer=ctx.tokenizer,
        )
        context_builder_params = {
            # False means using full community reports. True means using community short summaries.
            "use_community_summary": False,
            "shuffle_data": True,
            "include_community_rank": True,
            "min_community_rank": 0,
            "community_rank_name": "rank",
            "include_community_weight": True,
            "community_weight_name": "occurrence weight",
            "normalize_community_weight": True,
            # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 5000)
            "max_tokens": 12_000,
            "context_name": "Reports",
        }

        map_llm_params = {
            "max_tokens": 1000,
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
        }

        reduce_llm_params = {
            # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 1000-1500)
            "max_tokens": 2000,
            "temperature": 0.0,
        }
        return GlobalSearch(
            model=ctx.chat_model,
            context_builder=context_builder,
            tokenizer=ctx.tokenizer,
            # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 5000)
            max_data_tokens=12_000,
            map_llm_params=map_llm_params,
            reduce_llm_params=reduce_llm_params,
            # set this to True will add instruction to encourage the LLM to incorporate general knowledge in the response, which may increase hallucinations, but could be useful in some use cases.
            allow_general_knowledge=False,
            # set this to False if your LLM model does not support JSON mode.
            json_mode=True,
            context_builder_params=context_builder_params,
            concurrent_coroutines=32,
            # free form text describing the response type and format, can be anything, e.g. prioritized list, single paragraph, multiple paragraphs, multiple-page report
            response_type="multiple paragraphs",
        )
