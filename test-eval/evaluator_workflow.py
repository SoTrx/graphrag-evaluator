
from datetime import datetime
from pathlib import Path
from re import search
from typing import TypedDict

from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    GroundednessEvaluator,
    QAEvaluator,
    evaluate,
)
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ConnectionType,
    Evaluation,
    EvaluatorConfiguration,
    EvaluatorIds,
    InputDataset,
)
from azure.identity import DefaultAzureCredential
from graphrag.config.models.language_model_config import LanguageModelConfig

from adapters.aoai_configs_adapter import aoai_configs_adapter
from graph_sdk import GraphExplorer
from utils import console

CHAT_MODEL_CONFIG = "gpt5"
DATA_PATH = "assets/data.jsonl"
DEFAULT_THRESHOLD = 3


def run_evaluators(explorer: GraphExplorer, evaluation_model: AzureOpenAIModelConfiguration):

    groundedness_eval = GroundednessEvaluator(
        evaluation_model, threshold=DEFAULT_THRESHOLD)
    qa_eval = QAEvaluator(evaluation_model, threshold=DEFAULT_THRESHOLD)

    evaluation_result = evaluate(
        data=DATA_PATH,
        target=explorer.search,
        evaluators={
            "groundedness": groundedness_eval,
            "qa": qa_eval
        },
        evaluator_config={
            "default": {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${target.context_text}",
                    "response": "${target.response}"
                }
            }
        }
    )
    console.print(evaluation_result)
    console.print(
        f"\n[bold purple]✅ Evaluation for {explorer.model_deployment_name} Complete![/bold purple]")


def run_cloud_evaluators(dataset_path: Path, project_endpoint: str, deployment_name: str):

    dataset_name = f"graphrag_eval_{datetime.now().strftime('%d-%m-%Y_%Hh%Mm%Ss')}"
    DATASET_VERSION = "1.0.0"

    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential()
    )

    dataset = project_client.datasets.upload_file(
        name=dataset_name,
        version=DATASET_VERSION,
        file_path=str(dataset_path)
    )
    assert dataset.id is not None, "Dataset upload failed."

    evaluators = {
        "groundedness": EvaluatorConfiguration(
            id=EvaluatorIds.GROUNDEDNESS,
            init_params={"deployment_name": deployment_name},
            data_mapping={
                "query": "${data.query}",
                "context": "${data.context_text}",
                "response": "${data.response}"
            }
        ),
        # "qa": EvaluatorConfiguration(
        #     id=EvaluatorIds.QA,
        #     init_params={"deployment_name": deployment_name},
        #     data_mapping={
        #         "query": "${data.query}",
        #         "context": "${data.context_text}",
        #         "response": "${data.response}"
        #     }
        # ),
        "relevance": EvaluatorConfiguration(
            id=EvaluatorIds.RELEVANCE,
            init_params={"deployment_name": deployment_name},
            data_mapping={"response": "${data.response}",
                          "query": "${data.query}"}
        ),
    }
    evaluation = Evaluation(
        display_name="GraphRag Evaluation",
        description="Evaluation of GraphRag model responses using Groundedness and QA evaluators.",
        data=InputDataset(id=dataset.id),
        evaluators=evaluators
    )

    project_client.evaluations.create(
        evaluation,
        headers={
            "model-endpoint": f"https://{__get_resource_name_from_url(project_endpoint)}.cognitiveservices.azure.com/",
            # Note : On 1.1, only API key auth remote model endpoints
            "api-key": __get_api_key(project_client),
        }
    )


def __get_api_key(client: AIProjectClient) -> str:
    """
    Extract the API key from the default Azure OpenAI connection in the AIProjectClient.
    """
    connection = client.connections.get_default(
        connection_type=ConnectionType.AZURE_OPEN_AI, include_credentials=True
    )

    if connection.credentials.type != 'ApiKey':
        raise ValueError(
            f"Expected connection credentials type to be 'ApiKey', got {connection.credentials.type} instead."
        )
    return connection.credentials.api_key  # type: ignore


def __get_resource_name_from_url(url: str) -> str:
    """
    Extract the resource name from the Azure endpoint URL.
    Ex: https://xxys.services.ai.azure.com -> xxys
    """
    match = search(r"https://([^.]+)\.services\.ai\.azure\.com", url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract resource name from URL: {url}")
