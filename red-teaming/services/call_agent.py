from azure.ai.agents.models import Agent, ListSortOrder
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from app_config import settings

# project = AIProjectClient(
#     credential=DefaultAzureCredential(),
#     endpoint="https://aif-admin-justrebl-sw.services.ai.azure.com/api/projects/EvaluatorsTuto")

# agent = project.agents.get_agent("asst_Q9AHqwhu50snOkDpJ6Ws7QNu")


class AgentCaller:
    def __init__(self):
        self.project = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint=settings.project.azure_ai_project
        )
        self.agent = self.project.agents.get_agent(settings.project.agent_id)

    def call_agent(self, user_input: str) -> str:

        thread = self.project.agents.threads.create()
        print(f"Created thread, ID: {thread.id}")

        message = self.project.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        run = self.project.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=self.agent.id)

        last_message: str = ""

        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
        else:
            messages = self.project.agents.messages.list(
                thread_id=thread.id, order=ListSortOrder.ASCENDING)

            for message in messages:
                if message.text_messages:
                    last_message = (
                        f"{message.role}: {message.text_messages[-1].text.value}")

        print(last_message)

        return last_message
