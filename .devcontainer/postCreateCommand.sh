
#!/usr/bin/env bash
set -ex
echo "Running postCreateCommand..."
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Uv autocompletion
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc

# Dependency sync
cd test-eval && uv sync && cd -
cd red-teaming && uv sync && cd -
cd graph-mcp && uv sync && cd -
cd agents && uv sync && cd -
cd agent-framework-samples && uv sync && cd -
# Install graphviz for visualization

sudo apt update
sudo apt install graphviz -y