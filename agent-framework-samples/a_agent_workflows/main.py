# Copyright (c) Microsoft. All rights reserved.

import asyncio
from agent_framework import ConcurrentBuilder
from agent_framework.azure import AzureOpenAIChatClient
from azure.ai.agentserver.agentframework import from_agent_framework
# from azure.ai.agentserver.core import from_agent_framework
from azure.identity import DefaultAzureCredential


def main():
    # Create agents
    researcher = AzureOpenAIChatClient(credential=DefaultAzureCredential()).create_agent(
        instructions=(
            "You're an expert market and product researcher. "
            "Given a prompt, provide concise, factual insights, opportunities, and risks."
            "Start by stating your name as 'Market Researcher'."
        ),
        name="researcher",
    )
    marketer = AzureOpenAIChatClient(credential=DefaultAzureCredential()).create_agent(
        instructions=(
            "You're a creative marketing strategist. "
            "Craft compelling value propositions and target messaging aligned to the prompt."
            "Start by stating your name as 'Marketing Strategist'."
        ),
        name="marketer",
    )
    legal = AzureOpenAIChatClient(credential=DefaultAzureCredential()).create_agent(
        instructions=(
            "You're a cautious legal/compliance reviewer. "
            "Highlight constraints, disclaimers, and policy concerns based on the prompt."
            "Start by stating your name as 'Legal Reviewer'."
        ),
        name="legal",
    )

    # Build a concurrent workflow
    workflow = ConcurrentBuilder().participants(
        [researcher, marketer, legal]).build()

    # Convert the workflow to an agent
    workflow_agent = workflow.as_agent()

    # Run the agent as a hosted agent
    from_agent_framework(workflow_agent).run()


if __name__ == "__main__":
    main()
