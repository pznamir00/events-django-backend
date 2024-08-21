FROM python:3.8

ENV PYTHONUNBUFFERED=1
WORKDIR /code

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies with Poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry install

# Django gis dependencies
RUN apt-get update -y; \
    apt-get install -y gdal-bin; \
    apt-get update -y; \
    apt-get install -y python3-gdal; \
    apt-get update -y; \
    apt-get install -y rabbitmq-server;

# Copy source code
COPY . /code/
RUN chmod +x /code/scripts/bash/wait-for-it.sh
