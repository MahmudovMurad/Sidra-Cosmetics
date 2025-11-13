FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/root/.venv

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    # Translations dependencies
      gettext \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary from distroless image
COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /uvx /bin/

ARG APP_HOME=/code/sidra
WORKDIR $APP_HOME

# Install dependencies in a separate layer
COPY uv.lock pyproject.toml ./
RUN uv sync --locked --no-install-project

# Copy the rest of the application
COPY . ${APP_HOME}

# Sync the project
RUN uv sync --locked --no-install-project

# Copy and make executable start scripts
COPY ./docker/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/production/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]