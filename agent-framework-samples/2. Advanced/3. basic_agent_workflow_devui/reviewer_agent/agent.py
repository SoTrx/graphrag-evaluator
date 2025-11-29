import os

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv  # 📁 Secure configuration loading

load_dotenv()  # 📁 Load environment variables from .env file


chat_client = AzureOpenAIChatClient(credential=DefaultAzureCredential())

REVIEWER_NAME = "Concierge"
REVIEWER_INSTRUCTIONS = """
    You are an are hotel concierge who has opinions about providing the most local and authentic experiences for travelers.
    The goal is to determine if the front desk travel agent has recommended the best non-touristy experience for a traveler.
    If so, state that it is approved.
    If not, provide insight on how to refine the recommendation without using a specific example. 
    """

reviewer_agent = chat_client.create_agent(
    instructions=(
        REVIEWER_INSTRUCTIONS
    ),
    name=REVIEWER_NAME,
)
