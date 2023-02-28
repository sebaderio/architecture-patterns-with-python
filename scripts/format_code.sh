#! /usr/bin/env bash

set -e;

PATHS='src tests'

echo 'Running' $(black --version)
black --config pyproject.toml $PATHS
echo '----------------------------------------------------------------------'

echo 'Running isort' $(isort --version-number)
isort --settings-path pyproject.toml $PATHS
echo '----------------------------------------------------------------------'

echo 'Running' $(ruff --version)
ruff check --config pyproject.toml --fix --show-fixes $PATHS
echo '----------------------------------------------------------------------'

echo 'All linters ok!'
