"""GraphRAG search service for executing and displaying search results."""
from graph_sdk import GraphExplorer, SearchType


class GraphRagSearchService:
    """Service for performing GraphRAG searches and displaying results."""

    def __init__(self, explorer: GraphExplorer):
        """Initialize the search service with a GraphExplorer instance.

        Args:
            explorer: The GraphExplorer instance to use for searches
        """
        self.explorer = explorer

    async def search_and_print_results(self):
        """Search and print results from the graph explorer.

        Performs Local, Global, and Drift searches with predefined queries
        and prints the results to stdout.
        """
        # Local
        result = await self.explorer.search(SearchType.LOCAL, "Who is scrooge?")
        print(result.response)

        # Global
        result = await self.explorer.search(
            SearchType.GLOBAL, "What are the main themes of the story?"
        )
        print(result.response)

        # Drift
        result = await self.explorer.search(SearchType.DRIFT, "Who is scrooge?")
        print(result.response)
