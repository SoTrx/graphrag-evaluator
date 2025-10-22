# Evaluation Pipeline

Architecture flexible pour l'évaluation de modèles GraphRAG avec support de multiples évaluateurs.

## Architecture

### Structure des fichiers

```
test-eval/
├── config.py                      # Configuration centralisée
├── main.py                        # Point d'entrée principal
├── evaluators/                    # Évaluateurs
│   ├── __init__.py
│   ├── abstract_evaluator.py     # Classe abstraite de base
│   ├── retrieval_evaluator.py    # Évaluateur de récupération Azure
│   └── custom_metrics_evaluator.py # Exemple d'évaluateur personnalisé
├── pipeline/                      # Moteur de pipeline
│   ├── __init__.py
│   └── evaluation_pipeline.py    # Gestionnaire de pipeline
├── services/                      # Services GraphRAG
│   └── graphrag/
│       └── search_service.py
└── utils/                         # Utilitaires
    ├── env_utils.py
    └── pretty_print.py
```

## Utilisation

### 1. Configuration

La configuration est centralisée dans `config.py` et utilise les variables d'environnement :

```python
from config import initialize

config = initialize()  # Charge depuis les variables d'environnement
```

Variables requises :
- `AZURE_ENDPOINT`
- `AZURE_API_KEY`
- `AZURE_DEPLOYMENT_NAME`
- `AZURE_API_VERSION`

### 2. Créer un évaluateur personnalisé

Héritez de `AbstractEvaluator` :

```python
from evaluators.abstract_evaluator import AbstractEvaluator
from typing import Any, Dict

class MyCustomEvaluator(AbstractEvaluator):
    """Mon évaluateur personnalisé."""
    
    def _initialize(self) -> None:
        """Initialiser l'évaluateur avec la config."""
        # Accès à self.config pour la configuration
        self.my_setting = self.config.threshold
    
    async def evaluate(self, query: str, context: Any) -> Dict[str, Any]:
        """Évaluer le contexte."""
        # Votre logique d'évaluation
        return {
            "metric_1": {
                "score": 0.95,
                "reason": "Excellente qualité"
            },
            "metric_2": {
                "score": 0.80,
                "reason": "Bonne pertinence"
            }
        }
    
    @property
    def name(self) -> str:
        """Nom de l'évaluateur."""
        return "MyCustomEvaluator"
```

### 3. Construire un pipeline

```python
from config import initialize
from evaluators import RetrievalEvaluatorWrapper, CustomMetricsEvaluator
from pipeline import EvaluationPipeline
from utils import PrettyConsole

# Configuration
config = initialize()
console = PrettyConsole()

# Créer les évaluateurs
evaluators = [
    RetrievalEvaluatorWrapper(config),
    CustomMetricsEvaluator(config),
    MyCustomEvaluator(config),  # Votre évaluateur
]

# Créer le pipeline
pipeline = EvaluationPipeline(evaluators, console)
```

### 4. Exécuter le pipeline

```python
# Exécuter tous les évaluateurs
results = await pipeline.run(
    query="Ma question",
    context="Le contexte à évaluer",
    title="Mon évaluation"
)

# Accéder aux résultats par évaluateur
retrieval_result = results["RetrievalEvaluator"]
custom_result = results["MyCustomEvaluator"]
```

### 5. Gérer le pipeline dynamiquement

```python
# Ajouter un évaluateur
pipeline.add_evaluator(AnotherEvaluator(config))

# Supprimer un évaluateur
pipeline.remove_evaluator("CustomMetricsEvaluator")

# Lister les évaluateurs
names = pipeline.get_evaluator_names()
print(f"Évaluateurs actifs : {names}")

# Nombre d'évaluateurs
count = len(pipeline)
```

## Évaluateurs disponibles

### RetrievalEvaluatorWrapper
Wrapper pour l'évaluateur Azure AI de récupération. Évalue la qualité de la récupération d'information.

### CustomMetricsEvaluator
Exemple d'évaluateur personnalisé qui calcule des métriques basiques :
- Nombre de mots
- Nombre de caractères
- Vérification de longueur
- Vérification de contenu

## Exemple complet

```python
import asyncio
from config import initialize
from evaluators import RetrievalEvaluatorWrapper
from pipeline import EvaluationPipeline
from graph_sdk import GraphContext, GraphExplorer, SearchType

async def main():
    # Configuration
    config = initialize()
    
    # GraphRAG
    ctx = GraphContext(
        graph_path=config.gpt5_graph_path,
        aoia_endpoint=config.azure_endpoint,
        aoia_api_key=config.api_key,
    )
    explorer = GraphExplorer(ctx)
    
    # Pipeline
    pipeline = EvaluationPipeline([
        RetrievalEvaluatorWrapper(config),
    ])
    
    # Recherche
    query = "Ma question"
    context = await explorer.search(SearchType.LOCAL, query)
    
    # Évaluation
    results = await pipeline.run(query, context.response, "GPT-5")
    
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

## Avantages de cette architecture

1. **Extensible** : Ajoutez facilement de nouveaux évaluateurs
2. **Réutilisable** : Configuration centralisée et partagée
3. **Flexible** : Composez des pipelines personnalisés
4. **Maintenable** : Code organisé et documenté
5. **Testable** : Chaque évaluateur peut être testé indépendamment
