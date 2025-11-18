import asyncio
from pathlib import Path
from time import sleep

from azure.ai.agents.models import ListSortOrder
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from azure.ai.evaluation.red_team import AttackStrategy, RedTeam, RiskCategory
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from app_config import settings
from services.call_agent import AgentCaller
from utils import console


async def main():

    azure_ai_project = {
        "subscription_id": settings.project.subscription_id,
        "resource_group_name": settings.project.resource_group_name,
        "project_name": settings.project.project_name,
    }

    azure_ai_project = settings.project.azure_ai_project

    # Instantiate your AI Red Teaming Agent
    red_team_agent = RedTeam(
        azure_ai_project=azure_ai_project,  # required
        credential=DefaultAzureCredential()  # required
    )

    # A simple example application callback function that always returns a fixed response

    agent = AgentCaller()

    # def simple_callback(query: str) -> str:
    #     return "I'm an AI assistant that follows ethical guidelines. I cannot provide harmful content."

    # Runs a red teaming scan on the simple callback target
    red_team_result = await red_team_agent.scan(
        target=agent.call_agent,
        risk_categories=[
            RiskCategory.Violence,
            RiskCategory.HateUnfairness,
            RiskCategory.Sexual,
            RiskCategory.SelfHarm
        ],
        attack_strategies=[
            AttackStrategy.EASY,
            AttackStrategy.MODERATE,
            AttackStrategy.DIFFICULT
        ]
    )

    console.print(red_team_result)

if __name__ == "__main__":
    asyncio.run(main())
