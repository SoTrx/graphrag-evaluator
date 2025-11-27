import os 
from pathlib import Path

from agent_framework.openai import OpenAIChatClient  
from pydantic import BaseModel
from typing_extensions import Literal
from dotenv import load_dotenv  # 📁 Secure configuration loading

# Load environment variables from parent directory's .env file
env_path = Path(__file__).parent.parent / ".env"
print(f"Loading environment variables from: {env_path}")
load_dotenv(dotenv_path=env_path)


chat_client = OpenAIChatClient(
    base_url=os.environ.get("GITHUB_ENDPOINT"),    # 🌐 GitHub Models API endpoint
    api_key=os.environ.get("GITHUB_TOKEN"),        # 🔑 Authentication token
    model_id=os.environ.get("GITHUB_MODEL_ID")     # 🎯 Selected AI model
)

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


reviewer_agent = chat_client.create_agent(
    instructions=REVIEWER_INSTRUCTIONS,
    name=REVIEWER_NAME,
    response_format=ReviewAgent
)
