# GraphRAG Evaluator

A comprehensive repository demonstrating AI agent development, evaluation, and red teaming using Microsoft's Agent Framework and Azure AI services.

## 📁 Repository Structure

This repository contains four main components:

- **`evaluation/`** - Evaluate GraphRAG implementations using Azure AI Evaluation SDK
- **`red-teaming/`** - Test AI agents for safety and security using Azure AI Red Team tools
- **`agent-framework/`** - Samples and tutorials for building AI agents with Microsoft Agent Framework
- **`graph-mcp/`** - GraphRAG Model Context Protocol integration

## 🚀 Quick Start

### Prerequisites

- **Docker** - Required for dev container environment
- **VS Code** - Recommended for development
- **Azure Subscription** - For Azure OpenAI and Azure AI services
- **Python 3.10+** - Automatically configured in dev container

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd evaluation-sdk
   ```

2. **Open in Dev Container**
   - Open VS Code
   - Install the "Dev Containers" extension
   - Run: `Dev Containers: Reopen in Container`

3. **Configure environment variables**
   
   Each component requires its own configuration. Create `.env` files or configure `settings.toml` as needed:

## 📚 Components

### 1. Evaluation Pipeline (`evaluation/`)

Evaluate GraphRAG implementations against datasets using Azure AI Evaluation SDK.

**Features:**
- Query multiple GraphRAG implementations concurrently
- Generate evaluation datasets automatically
- Run local or cloud-based evaluators
- Evaluate groundedness and QA performance

**Setup:**
```bash
cd evaluation
```

Configure `settings.toml` with your Azure OpenAI endpoints:
```toml
[openai_defaults]
api_key = "your-api-key"
api_base = "your-endpoint"
api_version = "2025-01-01-preview"

[models.azure_openai_chat.gpt5]
model = "gpt-5-chat"
deployment_name = "gpt-5-chat"
```

**Run:**
```bash
python main.py
```

**What it does:**
1. Loads dataset from `assets/data.jsonl`
2. Queries configured GraphRAG implementations
3. Generates evaluation dataset
4. Runs evaluators (groundedness, QA)
5. Outputs evaluation metrics

### 2. Red Teaming (`red-teaming/`)

Test AI agents for safety vulnerabilities using Azure AI Red Team SDK.

**Features:**
- Automated adversarial testing
- Multiple attack strategies (easy, moderate, difficult)
- Risk category detection (violence, hate, sexual content, self-harm)

**Setup:**
```bash
cd red-teaming
```

Configure `settings.toml` with your Azure AI project:
```toml
[project]
subscription_id = "your-subscription-id"
resource_group_name = "your-resource-group"
project_name = "your-project-name"
agent_id = "your-agent-id"
```

**Run:**
```bash
python main.py
```

**What it does:**
1. Connects to your Azure AI project
2. Scans your agent for safety risks
3. Tests across multiple risk categories
4. Generates comprehensive safety report

### 3. Agent Framework Samples (`agent-framework/`)

Interactive tutorials for building AI agents with Microsoft Agent Framework.

**Samples:**
- `0.python-basic-agents.ipynb` - Create basic agents with different providers
- `1.python-tools.ipynb` - Add custom tools to agents
- `2.python-workflows.ipynb` - Build multi-agent workflows

**Advanced Examples:**
- Tracer and Aspire integration
- Agent workflows with DevUI
- Declarative agent configurations
- Azure deployment with `azd`

**Setup:**
```bash
cd agent-framework
```

Create `.env` file:
```env
# GitHub Models
GITHUB_TOKEN=your_github_token
GITHUB_ENDPOINT=https://models.inference.ai.azure.com
GITHUB_MODEL_ID=gpt-4o-mini

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your_deployment
```

**Run:**
Open any notebook in VS Code and follow the instructions:
- `1. Samples/0.python-basic-agents.ipynb` - Start here for basics
- `2. Advanced/` - Explore advanced patterns

## 🛠️ Development

### Install Dependencies

Each component manages its own dependencies via `pyproject.toml`:

```bash
# For evaluation
cd evaluation && uv sync

# For red-teaming
cd red-teaming && uv sync

# For agent-framework samples
cd agent-framework && uv sync
```

### Project Structure

```
evaluation-sdk/
├── evaluation/          # Evaluation pipeline
│   ├── main.py         # Entry point
│   ├── settings.toml   # Configuration
│   └── assets/         # Datasets
├── red-teaming/        # Safety testing
│   ├── main.py         # Entry point
│   └── settings.toml   # Configuration
├── agent-framework/    # Agent samples
│   ├── 1. Samples/     # Basic tutorials
│   └── 2. Advanced/    # Advanced patterns
└── tools/           
    └── 2. graphrag-mcp/    # GraphRAG MCP
```

## 📖 Additional Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/azure/ai-studio/agents/)
- [Azure AI Evaluation SDK](https://learn.microsoft.com/azure/ai-studio/how-to/develop/evaluate-sdk)
- [Azure AI Red Team](https://learn.microsoft.com/azure/ai-studio/how-to/develop/simulator-interaction-data)
- [GraphRAG Documentation](https://microsoft.github.io/graphrag/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

See LICENSE file for details.
