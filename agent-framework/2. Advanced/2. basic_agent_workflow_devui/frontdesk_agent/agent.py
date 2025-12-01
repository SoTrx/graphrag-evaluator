import os

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv  # 📁 Secure configuration loading

load_dotenv()  # 📁 Load environment variables from .env file


chat_client = AzureOpenAIChatClient(credential=DefaultAzureCredential())


FRONTDESK_NAME = "FrontDesk"
FRONTDESK_INSTRUCTIONS = """
    You are a Front Desk Travel Agent with ten years of experience and are known for brevity as you deal with many customers.
    The goal is to provide the best activities and locations for a traveler to visit.
    Only provide a single recommendation per response.
    You're laser focused on the goal at hand.
    Don't waste time with chit chat.
    Consider suggestions when refining an idea.
    """


front_desk_agent = chat_client.create_agent(
    instructions=(
        FRONTDESK_INSTRUCTIONS
    ),
    name=FRONTDESK_NAME,
)
