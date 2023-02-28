FROM python:3.11-slim-buster


RUN apt update && apt install curl -y

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.3.2

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
COPY src/ /app/src/

RUN $HOME/.local/bin/poetry config virtualenvs.create false && $HOME/.local/bin/poetry install
