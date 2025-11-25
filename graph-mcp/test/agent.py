from os import getenv

import pytest
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure import AzureOpenAIResponsesClient
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def chat_client():
    """Fixture to provide an Azure OpenAI chat client."""
    return AzureOpenAIResponsesClient(
        deployment_name=getenv("CHAT_DEPLOYMENT_NAME", "gpt-5.0"),
        endpoint=getenv("CHAT_DEPLOYMENT_URL", None),
        api_key=getenv("CHAT_API_KEY", None),
    )


@pytest.mark.asyncio
async def test_e2e_http_mcp_agent_query(chat_client):
    """Test querying the MCP server through the agent.

    NOTE: THIS IS AN END-TO-END TEST AND REQUIRES THE MCP SERVER TO BE RUNNING LOCALLY.
    PLEASE START THE MCP SERVER BEFORE RUNNING THIS TEST.

    """
    async with (
        MCPStreamableHTTPTool(
            name="A christmas carol knowledge graph",
            url="http://localhost:8000/mcp",
        ) as mcp_server,
        ChatAgent(
            chat_client=chat_client,
            name="Retrieval agent",
            instructions="You know everything about 'A christmas carol' and can answer questions about it.",
        ) as agent,
    ):
        result = await agent.run(
            "Who is Scrooge's business partner?",
            tools=mcp_server
        )
        assert result is not None, "Agent should return a result"
