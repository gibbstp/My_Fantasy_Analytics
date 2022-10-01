FROM python:3.11.0b3-bullseye

RUN apt-get update && \
    apt-get update -y && \
    pip install --upgrade pip

WORKDIR /home/poetry

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    POETRY_HOME="/home/poetry" && \    
    POETRY_VIRTUALENVS_CREATE=false
    
ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml poetry.lock ./
    
RUN poetry install