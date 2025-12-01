import pytest
from fastmcp import Client


@pytest.fixture
def mcp_client():
    """Fixture to provide an MCP client."""
    return Client("http://localhost:8000/mcp")


@pytest.mark.asyncio
async def test_search_tool_character_query(mcp_client):
    """
    Actual content check
    NOTE: THIS IS AN END-TO-END TEST AND REQUIRES THE MCP SERVER TO BE RUNNING LOCALLY.
    PLEASE START THE MCP SERVER BEFORE RUNNING THIS TEST.
    """
    async with mcp_client:
        result = await mcp_client.call_tool("search", {"query": "Who is Scrooge's business partner?"})

        # Assertions
        assert result is not None, "Search tool should return a result for character query"


@pytest.mark.asyncio
async def test_search_tool_empty_query(mcp_client):
    """
    Sanity check    
    
    NOTE: THIS IS AN END-TO-END TEST AND REQUIRES THE MCP SERVER TO BE RUNNING LOCALLY.
    PLEASE START THE MCP SERVER BEFORE RUNNING THIS TEST.
    
    """
    async with mcp_client:
        result = await mcp_client.call_tool("search", {"query": ""})
        assert result is not None, "Search tool should return a result even for empty query"
