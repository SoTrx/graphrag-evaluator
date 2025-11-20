
import logging
from pathlib import Path
from re import search
from typing import Callable, Dict, Optional

from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    EvaluationResult,
    EvaluatorConfig,
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


def evaluate_locally(dataset: Path, evaluation_model: AzureOpenAIModelConfiguration, target: Optional[Callable] = None) -> EvaluationResult:
    """
    Run evaluators locally on the provided dataset using the specified evaluation model.
    If a target function is provided, it will be used to generate model responses for evaluation.
    Otherwise, it is assumed that the dataset already contains model responses.

    Parameters:
    - dataset (Path): Path to the dataset file containing queries and context.
    - evaluation_model (AzureOpenAIModelConfiguration): Configuration for the evaluation model.
    - target (Optional[Callable]): A callable that generates model responses for evaluation.

    Returns:
    - EvaluationResult: The result of the evaluation containing scores from the evaluators.
    """

    # Use the target results as response for evaluation
    config: Dict[str, EvaluatorConfig] = {
        "default": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${target.context_text}",
                "response": "${target.response}"
            }
        }
    }
    if target is None:
        logging.debug(
            "No target function provided for evaluation"
            " Assuming dataset already contains model responses."
        )
        # Assume dataset already contains model responses
        config = {
            "default": {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${data.context_text}",
                    "response": "${data.response}"
                }
            }
        }

    return evaluate(
        data=dataset,
        target=target,
        evaluators={
            "groundedness": GroundednessEvaluator(evaluation_model),
            "qa": QAEvaluator(evaluation_model)
        },
        evaluator_config=config
    )


def evaluate_cloud(dataset: Path, project_endpoint: str, judge_deployment_name: str) -> None:
    """
    Run evaluators in Azure AI Projects on the provided dataset using the specified judge model deployment.
    Parameters:
    - dataset (Path): Path to the dataset file containing queries and context.
    - project_endpoint (str): The endpoint URL of the Azure AI Projects instance.
    - judge_deployment_name (str): The name of the model deployment to be used for
      evaluation.

    """

    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential()
    )

    uploaded_dataset = __upload_dataset(project_client, dataset)

    evaluation = Evaluation(
        display_name="GraphRag Evaluation",
        description="Evaluation of GraphRag model responses using Groundedness and QA evaluators.",
        data=InputDataset(id=uploaded_dataset),
        evaluators={
            "groundedness": EvaluatorConfiguration(
                id=EvaluatorIds.GROUNDEDNESS,
                init_params={"deployment_name": judge_deployment_name},
                data_mapping={
                    "query": "${data.query}",
                    "context": "${data.context_text}",
                    "response": "${data.response}"
                }
            ),
            "relevance": EvaluatorConfiguration(
                id=EvaluatorIds.RELEVANCE,
                init_params={"deployment_name": judge_deployment_name},
                data_mapping={
                    "response": "${data.response}",
                    "query": "${data.query}"
                }
            ),
        }
    )

    project_client.evaluations.create(
        evaluation,
        headers={
            "model-endpoint": f"https://{__get_resource_name_from_url(project_endpoint)}.cognitiveservices.azure.com/",
            # Note : On 1.1, only API key auth remote model endpoints
            "api-key": __get_api_key(project_client),
        }
    )


def __upload_dataset(client: AIProjectClient, dataset: Path) -> str:
    """
    Upload a dataset file to Foundry. Replaces any existing dataset with the same name and version.
    Returns the ID of the uploaded dataset artifact.
    """
    DATASET_VERSION = "1.0.0"
    client.datasets.delete(name=dataset.stem, version=DATASET_VERSION)
    artifact = client.datasets.upload_file(
        name=dataset.name,
        version=DATASET_VERSION,
        file_path=str(dataset)
    )

    assert artifact.id is not None, "Dataset upload failed."

    return artifact.id


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
