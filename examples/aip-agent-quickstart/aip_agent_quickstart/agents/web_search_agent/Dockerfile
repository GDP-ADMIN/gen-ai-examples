ARG PYTHON_VERSION=3.13.3
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/usr/src/app
ENV POETRY_HOME=/opt/poetry
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PIP_DEFAULT_TIMEOUT=100

# Install poetry
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to PATH
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Create non-root user
ARG APP_USER=web_search_agentuser
RUN groupadd -r ${APP_USER} && useradd --create-home -r -g ${APP_USER} ${APP_USER}

# Create and set permissions for poetry cache, to be owned by APP_USER.
# Poetry might use this if configured, or its defaults.
# It's good practice to ensure it's writable if we expect venvs here.
RUN mkdir -p ${POETRY_CACHE_DIR}/virtualenvs && \
    chown -R ${APP_USER}:${APP_USER} ${POETRY_CACHE_DIR} && \
    chmod -R u+rwx,g+rwx ${POETRY_CACHE_DIR}

WORKDIR ${APP_HOME}
# APP_HOME is now created and owned by root.

# Copy dependency definition files (into APP_HOME)
COPY pyproject.toml poetry.lock* ./

# Install project dependencies as root.
# Poetry will create/manage its virtual environment according to its defaults
# or pyproject.toml settings (e.g., virtualenvs.in-project).
# If it creates a .venv here, it will be chowned later.
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code (into APP_HOME)
COPY ./ ./

# Set final permissions for the entire app directory (including any .venv)
# and the poetry cache directory.
RUN chown -R ${APP_USER}:${APP_USER} ${APP_HOME} && \
    chown -R ${APP_USER}:${APP_USER} ${POETRY_CACHE_DIR} # Re-affirm cache ownership

USER ${APP_USER}

EXPOSE 8002

# Run the agent server
CMD ["poetry", "run", "python", "-m", "server", "--host", "0.0.0.0", "--port", "8002"]
