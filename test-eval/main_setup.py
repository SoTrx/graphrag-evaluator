from pathlib import Path

from app_config import settings
from config import load_queries
from config.model_factory import ModelFactory
from graph_sdk import GraphExplorer
from graphrag.config.enums import ModelType
from utils import console


def initialize() -> tuple[list[str], ModelFactory, list[GraphExplorer]]:
    # Initialize configuration and GraphRAG contexts
    console.print(
        "[yellow]⚙️  Loading configuration and initializing GraphRAG contexts...[/yellow]")

    queries = load_queries()
    model_factory = ModelFactory()
    graph_explorers = initialize_graph_explorers(model_factory)

    return queries, model_factory, graph_explorers


def initialize_graph_explorers(model_factory: ModelFactory):
    graph_explorers: list[GraphExplorer] = []

    for model_name in model_factory.list_models(ModelType.AzureOpenAIChat):

        chat_model = model_factory.get(model_name, ModelType.AzureOpenAIChat)
        embedding_model = model_factory.get(
            "large", ModelType.AzureOpenAIEmbedding)
        
        # Skip if models are not properly configured
        if chat_model is None or embedding_model is None:
            console.print(f"[yellow]⚠️  Skipping {model_name}: Missing model configuration[/yellow]")
            continue
            
        graph_path = settings.evaluations[model_name].path

        graph_explorer = GraphExplorer(
            graph_path=Path(graph_path),
            chat_config=chat_model,
            embedding_config=embedding_model
        )

        graph_explorers.append(graph_explorer)

    return graph_explorers
