FROM python:3.13-slim

# Install required system packages
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.1.3
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set workdir
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies (no dev by default)
RUN poetry install

# Expose API port for Traefik
EXPOSE 8000

# Create database seed
RUN poetry run task seed

# Start the API via task (e.g. task serve_prod)
CMD ["poetry", "run", "task", "serve_prod"]