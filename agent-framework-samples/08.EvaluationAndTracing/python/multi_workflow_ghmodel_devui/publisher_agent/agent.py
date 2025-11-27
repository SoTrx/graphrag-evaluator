import os 
from pathlib import Path

from agent_framework.openai import OpenAIChatClient  
from agent_framework import HostedCodeInterpreterTool
from pydantic import BaseModel
from dotenv import load_dotenv  # 📁 Secure configuration loading

# Load environment variables from parent directory's .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


chat_client = OpenAIChatClient(
    base_url=os.environ.get("GITHUB_ENDPOINT"),    # 🌐 GitHub Models API endpoint
    api_key=os.environ.get("GITHUB_TOKEN"),        # 🔑 Authentication token
    model_id=os.environ.get("GITHUB_MODEL_ID")     # 🎯 Selected AI model
)

PUBLISHER_NAME = "Publisher"
PUBLISHER_INSTRUCTIONS = """
You are the content publisher, run code to save the tutorial's draft content as a Markdown file. Saved file's name is marked with current date and time, such as yearmonthdayhourminsec. Note that if it is 1-9, you need to add 0, such as  20240101123045.md.
"""


class PublisherAgent(BaseModel):
    file_path: str


publisher_agent = chat_client.create_agent(
    instructions=PUBLISHER_INSTRUCTIONS,
    tools=HostedCodeInterpreterTool(),
    name=PUBLISHER_NAME,
    response_format=PublisherAgent
)
