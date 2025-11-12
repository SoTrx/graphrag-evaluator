
from adapters.aoai_configs_adapter import aoai_configs_adapter
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    GroundednessEvaluator,
    QAEvaluator,
    evaluate,
)
from graph_sdk import GraphExplorer
from graphrag.config.models.language_model_config import LanguageModelConfig
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
