FROM python:3.13-slim

WORKDIR /app

# Copy poetry configuration
COPY pyproject.toml ./

# Install Poetry and dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy application code
COPY . ./

# Expose the server port
EXPOSE 8002

# Start the server
CMD ["python", "server.py"]
