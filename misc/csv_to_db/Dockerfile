FROM python:3.12.5-bullseye

RUN apt-get update && \
    apt-get update -y && \
    pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -
    
ENV PATH="${PATH}:/root/.local/bin" \
    POETRY_HOME="/home/poetry" \    
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /home

COPY poetry.lock pyproject.toml ./

RUN poetry export --output requirements.txt --with dev --without-hashes && \
    pip install -r requirements.txt