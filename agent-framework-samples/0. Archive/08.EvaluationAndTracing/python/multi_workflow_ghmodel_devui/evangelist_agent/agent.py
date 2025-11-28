import os 
from pathlib import Path

from agent_framework.openai import OpenAIChatClient  
from agent_framework import HostedWebSearchTool
from pydantic import BaseModel
from dotenv import load_dotenv  # 📁 Secure configuration loading

# Load environment variables from parent directory's .env file
env_path = Path(__file__).parent.parent / ".env"

print(f"Loading environment variables from: {env_path}")
load_dotenv(dotenv_path=env_path)


chat_client = OpenAIChatClient(
    base_url=os.environ.get("GITHUB_ENDPOINT"), 
    api_key=os.environ.get("GITHUB_TOKEN"), 
    model_id=os.environ.get("GITHUB_MODEL_ID")
)

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


evangelist_agent = chat_client.create_agent(
    instructions=EVANGELIST_INSTRUCTIONS,
    tools=[HostedWebSearchTool()],
    name=EVANGELIST_NAME,
    response_format=EvangelistAgent,
)
