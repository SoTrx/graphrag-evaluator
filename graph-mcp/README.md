# Graph MCP Server

A Model Context Protocol (MCP) server that provides knowledge graph functionality for "A Christmas Carol".

## Setup

Install dependencies:

```bash
uv sync --group dev
```

## Running the Server

Start the MCP server:

```bash
uv run server.py
```

The server will be available at `http://localhost:8000/mcp`.

## Testing

The project uses pytest for testing. Tests are located in the `test/` directory.

### Prerequisites

Make sure the MCP server is running before executing the tests:

```bash
uv run server.py
```

### Running Tests

Run all tests:

```bash
uv run pytest
```

Run specific test file:

```bash
uv run pytest test/agent.py
uv run pytest test/tool_usage.py
```

Run with verbose output:

```bash
uv run pytest -v
```

Run specific test function:

```bash
uv run pytest test/agent.py::test_http_mcp_agent_query -v
```

### Test Structure

- `test/agent.py` - Tests for the agent framework integration with the MCP server
- `test/tool_usage.py` - Tests for direct MCP tool usage via FastMCP client
- `test/conftest.py` - Shared pytest fixtures and configuration

### Running Tests in VS Code

The project is configured to work with VS Code's Testing view:

1. Open the Testing view (flask icon in the sidebar)
2. Tests should automatically be discovered
3. Click the play button next to any test to run it
4. If tests don't appear, click the "Refresh Tests" button in the Testing view

**Note**: Make sure the Python interpreter is set to `.venv/bin/python` in the workspace.

### Troubleshooting

If tests are not discovered in VS Code:
1. Check that the Python interpreter is set correctly (Command Palette → "Python: Select Interpreter")
2. Refresh test discovery (Testing view → Refresh button)
3. Verify pytest is installed: `uv sync --group dev`
4. Check the Output panel → "Python Test Log" for errors

### Environment Variables

Required environment variables for tests:

- `CHAT_DEPLOYMENT_NAME` - Azure OpenAI deployment name (default: "gpt-5.0")
- `CHAT_DEPLOYMENT_URL` - Azure OpenAI endpoint URL
- `CHAT_API_KEY` - Azure OpenAI API key

Create a `.env` file in the project root with these variables.

## Project Structure

```
graph-mcp/
├── server.py           # MCP server implementation
├── graph/              # GraphRAG data and configurations
├── graph_sdk/          # Graph SDK modules
├── test/               # Test files
│   ├── agent.py        # Agent integration tests
│   ├── tool_usage.py   # Tool usage tests
│   └── conftest.py     # Shared test fixtures
├── pyproject.toml      # Project dependencies
└── pytest.ini          # Pytest configuration
```
