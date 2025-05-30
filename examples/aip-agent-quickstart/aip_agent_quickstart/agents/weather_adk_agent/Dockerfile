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
ARG APP_USER=agentuser
RUN groupadd -r ${APP_USER} && useradd --no-create-home -r -g ${APP_USER} ${APP_USER}

WORKDIR ${APP_HOME}

# Configure poetry and create cache directory
RUN mkdir -p ${POETRY_CACHE_DIR}/virtualenvs && \
    chmod -R 775 ${POETRY_CACHE_DIR}

# Copy dependency definition files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
# --no-interaction: Do not ask any interactive questions
# --no-ansi: Disable ANSI output
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY ./ ./

# Set permissions for app and cache directories
RUN chown -R ${APP_USER}:${APP_USER} ${APP_HOME} && \
    chown -R ${APP_USER}:${APP_USER} ${POETRY_CACHE_DIR}
USER ${APP_USER}

EXPOSE 8004

# Run the weather agent server
CMD ["poetry", "run", "python", "-m", "server"]
