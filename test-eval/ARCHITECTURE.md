# Architecture du Pipeline d'Évaluation

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────────┐
│                            main.py                                  │
│                      (Point d'entrée)                               │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
┌───────────────────────────┐   ┌───────────────────────────────────┐
│      config.py            │   │    GraphRAG (graph_sdk)           │
│  EvaluationConfig         │   │  - GraphContext                   │
│  - initialize()           │   │  - GraphExplorer                  │
│  - from_env()             │   │  - SearchType                     │
│  - get_model_config()     │   │                                   │
└───────────┬───────────────┘   └───────────────┬───────────────────┘
            │                                   │
            │                                   │ Search Results
            │                                   │
            │                   ┌───────────────▼───────────────┐
            │                   │                               │
            │                   │   Context Response            │
            │                   │   (search results)            │
            │                   │                               │
            │                   └───────────────┬───────────────┘
            │                                   │
            ▼                                   │
┌───────────────────────────────────────────────┼───────────────┐
│         EvaluationPipeline                    │               │
│         (pipeline/evaluation_pipeline.py)     │               │
│                                               │               │
│  + __init__(evaluators, console)              │               │
│  + run(query, context, title) ────────────────┘               │
│  + add_evaluator(evaluator)                                   │
│  + remove_evaluator(name)                                     │
│  + get_evaluator_names()                                      │
│                                                               │
│  Orchestrates multiple evaluators ──────┐                    │
└──────────────────────────────────────────┼────────────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
        ┌───────────────────┐  ┌───────────────────┐  ┌──────────────────┐
        │ AbstractEvaluator │  │ AbstractEvaluator │  │ AbstractEvaluator│
        │      (ABC)        │  │      (ABC)        │  │      (ABC)       │
        └─────────┬─────────┘  └─────────┬─────────┘  └────────┬─────────┘
                  │                      │                      │
                  │                      │                      │
        ┌─────────▼──────────┐ ┌────────▼──────────┐ ┌────────▼─────────┐
        │ Retrieval          │ │ CustomMetrics     │ │  Your Custom     │
        │ EvaluatorWrapper   │ │ Evaluator         │ │  Evaluator       │
        │                    │ │                   │ │                  │
        │ Azure AI           │ │ Word count        │ │ Implement:       │
        │ Retrieval API      │ │ Char count        │ │ - _initialize()  │
        │                    │ │ Length checks     │ │ - evaluate()     │
        │                    │ │                   │ │ - name property  │
        └────────────────────┘ └───────────────────┘ └──────────────────┘
```

## Flux d'exécution

```
1. Configuration
   └─> config.initialize()
       └─> EvaluationConfig.from_env(load_or_die)
           └─> Charge les variables d'environnement

2. Initialisation GraphRAG
   └─> GraphContext(config.gpt5_graph_path, ...)
       └─> GraphExplorer(context)

3. Construction du Pipeline
   └─> evaluators = [Evaluator1(config), Evaluator2(config), ...]
       └─> pipeline = EvaluationPipeline(evaluators, console)

4. Recherche
   └─> context = await explorer.search(SearchType.LOCAL, query)

5. Évaluation
   └─> results = await pipeline.run(query, context.response, "Title")
       └─> Pour chaque evaluator dans evaluators:
           ├─> result = await evaluator.evaluate(query, context)
           └─> console.print_evaluation_result(title, result)
```

## Classe AbstractEvaluator (ABC)

```python
class AbstractEvaluator(ABC):
    
    def __init__(self, config: EvaluationConfig)
        ├─> self.config = config
        └─> self._initialize()
    
    @abstractmethod
    def _initialize(self) -> None
        └─> Implémenté par les sous-classes
    
    @abstractmethod
    async def evaluate(self, query: str, context: Any) -> Dict[str, Any]
        └─> Implémenté par les sous-classes
        └─> Retourne: {"metric_name": {"score": X, "reason": "..."}}
    
    @property
    @abstractmethod
    def name(self) -> str
        └─> Retourne le nom de l'évaluateur
```

## Implémentation d'un évaluateur personnalisé

```
1. Hériter de AbstractEvaluator
   └─> class MyEvaluator(AbstractEvaluator)

2. Implémenter _initialize()
   └─> Accéder à self.config
   └─> Initialiser ressources, modèles, etc.

3. Implémenter evaluate(query, context)
   └─> Logique d'évaluation
   └─> Retourner Dict[str, Any] avec métriques

4. Implémenter name property
   └─> Retourner un nom unique

5. Ajouter au pipeline
   └─> evaluators.append(MyEvaluator(config))
```

## Utilisation des utilitaires

```
utils/
├── PrettyConsole
│   ├── print_context(title, response, obj)
│   ├── print_evaluation_result(title, result)
│   └── print(*args, **kwargs)
│
└── load_or_die(key)
    └─> Charge variable d'environnement ou échoue
```

## Exemple de résultat d'évaluation

```python
{
    "RetrievalEvaluator": {
        "gpt_groundedness": {
            "score": 5,
            "reason": "The response is well grounded..."
        },
        "gpt_relevance": {
            "score": 4,
            "reason": "The response is relevant..."
        }
    },
    "CustomMetricsEvaluator": {
        "word_count": {
            "score": 250,
            "reason": "Response contains 250 words"
        },
        "length_check": {
            "score": 1,
            "reason": "Length is within acceptable range"
        }
    }
}
```
