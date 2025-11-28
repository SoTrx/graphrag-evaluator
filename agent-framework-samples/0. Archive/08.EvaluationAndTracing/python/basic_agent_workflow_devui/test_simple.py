#!/usr/bin/env python3
"""Simple test script to debug the serialization issue."""

import logging
import os
from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatClient
from agent_framework import WorkflowBuilder

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Test workflow creation and serving."""
    try:
        # Create chat client
        chat_client = OpenAIChatClient(
            base_url=os.environ.get("GITHUB_ENDPOINT"),
            api_key=os.environ.get("GITHUB_TOKEN"),
            model_id=os.environ.get("GITHUB_MODEL_ID")
        )
        
        # Create simple agents
        agent1 = chat_client.create_agent(
            instructions="You are a helpful travel agent.",
            name="TravelAgent"
        )
        
        agent2 = chat_client.create_agent(
            instructions="You are a reviewer.",
            name="Reviewer"
        )
        
        # Create workflow
        workflow = WorkflowBuilder().set_start_executor(agent1).add_edge(agent1, agent2).build()
        
        logger.info("Workflow created successfully")
        
        # Try to serve
        from agent_framework.devui import serve
        logger.info("Starting server...")
        serve(entities=[workflow], port=8090, auto_open=False)
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()