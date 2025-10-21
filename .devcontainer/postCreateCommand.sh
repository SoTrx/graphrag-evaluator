
#!/usr/bin/env bash
set -ex
echo "Running postCreateCommand..."
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Uv autocompletion
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
cd test-eval && uv sync 