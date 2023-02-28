#! /usr/bin/env bash

set -e;

PATHS='src tests'

echo 'Running' $(black --version)
black --config pyproject.toml --diff --check $PATHS
echo '----------------------------------------------------------------------'

echo 'Running isort' $(isort --version-number)
isort --settings-path pyproject.toml --check-only --diff $PATHS
echo '----------------------------------------------------------------------'

echo 'Running' $(ruff --version)
ruff check --config pyproject.toml $PATHS
echo '----------------------------------------------------------------------'

echo 'All linters ok!'
