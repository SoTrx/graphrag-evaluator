"""Evangelist Agent - Azure AI Foundry with Bing Search Tool"""

import asyncio
import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

from azure.ai.agents.models import BingGroundingTool


from azure.identity.aio import AzureCliCredential
from azure.ai.projects.aio import AIProjectClient

from agent_framework import HostedWebSearchTool, ChatAgent
from agent_framework.azure import AzureAIAgentClient

# Load environment variables from parent directory's .env file
env_path = Path(__file__).parent.parent / ".env"
print(f"🔧 [Evangelist] Loading environment from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Agent configuration
EVANGELIST_NAME = "Evangelist"
EVANGELIST_INSTRUCTIONS = """
You are a technology evangelist create a first draft for a technical tutorials.
    1. Each knowledge point in the outline must include a link. Follow the link to access the content related to the knowledge point in the outline. Expand on that content.
    2. Each knowledge point must be explained in detail.
    3. Rewrite the content according to the entry requirements, including the title, outline, and corresponding content. It is not necessary to follow the outline in full order.
    4. The content must be more than 200 words.
    5. Always return JSON with draft_content (string) "
    6. Include draft_content in draft_content"
"""


class EvangelistAgent(BaseModel):
    """Represents the result of draft content"""
    draft_content: str


# Configuration for agent creation
BING_CONNECTION_ID = os.environ["BING_CONNECTION_ID"]
# _credential = AzureCliCredential()
# _client = AIProjectClient(
#             endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
#             credential=_credential
#         )
    # Initialize Bing Grounding tool
bing = BingGroundingTool(connection_id=BING_CONNECTION_ID)

# async def create_evangelist_agent():
#     """
#     Create evangelist agent with Azure AI Foundry
    
#     Args:
#         client: AIProjectClient instance (must remain open during workflow execution)
#     """
#     # Initialize Bing Grounding tool
#     bing = BingGroundingTool(connection_id=BING_CONNECTION_ID)
    
#     # Create agent with Bing Search
#     created_agent =await _client.agents.create_agent(
#         model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
#         instructions=EVANGELIST_INSTRUCTIONS,
#         name=EVANGELIST_NAME,
#         tools=bing.definitions
#     )
    
#     print(f"✅ [Evangelist] Agent created with ID: {created_agent.id}")
    
#     # Create chat client
#     chat_client = AzureAIAgentClient(
#         project_client=_client,
#         agent_id=created_agent.id,
#         tools=bing.definitions,
#         response_format=EvangelistAgent
#     )
    
#     # Create and return the ChatAgent with hosted web search tool
#     return ChatAgent(
#         chat_client=chat_client,
#         tools=HostedWebSearchTool()
#     )


# Create agent instance at module level (following Agent Framework conventions)
agent = ChatAgent(
    name=EVANGELIST_NAME,
    chat_client=AzureAIAgentClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        model_deployment_name=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        async_credential=AzureCliCredential(),
        tools = bing.definitions,
        response_format=EvangelistAgent,
    ),
    instructions=EVANGELIST_INSTRUCTIONS,
    tools=HostedWebSearchTool()
)



# agent = asyncio.run(create_evangelist_agent())
