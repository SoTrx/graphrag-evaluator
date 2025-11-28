"""Content Reviewer Agent - Azure AI Foundry Basic Agent"""
import asyncio
import os
from pathlib import Path
from pydantic import BaseModel
from typing_extensions import Literal
from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient

from azure.identity.aio import AzureCliCredential
from azure.ai.projects.aio import AIProjectClient

# Load environment variables from parent directory's .env file
env_path = Path(__file__).parent.parent / ".env"
print(f"🔧 [Reviewer] Loading environment from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Agent configuration
REVIEWER_NAME = "ContentReviewer"
REVIEWER_INSTRUCTIONS = """
You are a content reviewer and need to check whether the tutorial's draft content meets the following requirements:

1. The draft content less than 200 words, set 'review_result' to 'No' and 'reason' to 'Content is too short'. If the draft content is more than 200 words, set 'review_result' to 'Yes' and 'reason' to 'The content is good'.
2. set 'draft_content' to the original draft content.
3. Always return result as JSON with fields 'review_result' ('Yes' or  'No' ) and 'reason' (string) and 'draft_content' (string).
"""


class ReviewAgent(BaseModel):
    review_result: Literal["Yes", "No"]
    reason: str
    draft_content: str


# _credential = AzureCliCredential()
# _client = AIProjectClient(
#             endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
#             credential=_credential
#         )


# async def create_reviewer_agent():
#     """
#     Create reviewer agent with Azure AI Foundry
    
#     Args:
#         client: AIProjectClient instance (must remain open during workflow execution)
#     """
#     # Create basic agent without special tools
#     created_agent =await _client.agents.create_agent(
#         model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
#         instructions=REVIEWER_INSTRUCTIONS,
#         name=REVIEWER_NAME
#     )
    
#     print(f"✅ [Reviewer] Agent created with ID: {created_agent.id}")
    
#     # Create chat client
#     chat_client = AzureAIAgentClient(
#         project_client=_client,
#         agent_id=created_agent.id,
#         response_format=ReviewAgent
#     )
    
#     # Create and return the ChatAgent without tools
#     return ChatAgent(chat_client=chat_client)

agent = ChatAgent(
    name=REVIEWER_NAME,
    chat_client=AzureAIAgentClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        model_deployment_name=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        async_credential=AzureCliCredential(),
        response_format=ReviewAgent,
    ),
    instructions=REVIEWER_INSTRUCTIONS,
)

# agent = asyncio.run(create_reviewer_agent())
