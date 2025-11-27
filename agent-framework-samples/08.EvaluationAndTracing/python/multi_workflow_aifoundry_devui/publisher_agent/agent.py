"""Publisher Agent - Azure AI Foundry with Code Interpreter Tool"""

import asyncio
import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

from azure.ai.agents.models import CodeInterpreterTool


from azure.identity.aio import AzureCliCredential
from azure.ai.projects.aio import AIProjectClient

from agent_framework import HostedCodeInterpreterTool, ChatAgent
from agent_framework.azure import AzureAIAgentClient

# Load environment variables from parent directory's .env file
env_path = Path(__file__).parent.parent / ".env"
print(f"🔧 [Publisher] Loading environment from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Agent configuration
PUBLISHER_NAME = "Publisher"
PUBLISHER_INSTRUCTIONS = """
You are the content publisher ,run code to save the tutorial's draft content as a Markdown file. Saved file's name is marked with current date and time, such as yearmonthdayhourminsec. Note that if it is 1-9, you need to add 0, such as  20240101123045.md.
set 'file_path' to save path .Always return result as JSON with fields 'file_path' (string )
"""


class PublisherAgent(BaseModel):
    file_path: str


# _credential = AzureCliCredential()
# _client = AIProjectClient(
#             endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
#             credential=_credential
#         )


# async def create_publisher_agent():
#     """
#     Create publisher agent with Azure AI Foundry
    
#     Args:
#         client: AIProjectClient instance (must remain open during workflow execution)
#     """
#     # Initialize Code Interpreter tool
#     code_interpreter = CodeInterpreterTool()
    
#     # Create agent with Code Interpreter
#     created_agent = await _client.agents.create_agent(
#         model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
#         instructions=PUBLISHER_INSTRUCTIONS,
#         name=PUBLISHER_NAME,
#         tools=code_interpreter.definitions
#     )
    
#     print(f"✅ [Publisher] Agent created with ID: {created_agent.id}")
    
#     # Create chat client
#     chat_client = AzureAIAgentClient(
#         project_client=_client,
#         agent_id=created_agent.id,
#         response_format=PublisherAgent
#     )
    
#     # Create and return the ChatAgent with hosted code interpreter tool
#     return ChatAgent(
#         chat_client=chat_client,
#         tools=HostedCodeInterpreterTool()
#     )
    # Initialize Code Interpreter tool
code_interpreter = CodeInterpreterTool()

agent = ChatAgent(
    name="Publisher",
    chat_client=AzureAIAgentClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        model_deployment_name=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        async_credential=AzureCliCredential(),
        response_format=PublisherAgent,
        tools=code_interpreter.definitions
    ),
    instructions="""
    You are the content publisher, run code to save the tutorial's draft content as a Markdown file.
    Saved file's name is marked with current date and time, such as yearmonthdayhourminsec.
    Note that if it is 1-9, you need to add 0, such as 20240101123045.md.
    set 'file_path' to save path. Always return result as JSON with fields 'file_path' (string)
    """,
    tools=HostedCodeInterpreterTool(),
)


# agent = asyncio.run(create_publisher_agent())
