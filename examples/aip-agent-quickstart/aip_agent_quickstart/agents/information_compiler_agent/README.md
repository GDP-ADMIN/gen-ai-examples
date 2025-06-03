# InformationCompilerAgent Agent

This is the an A2A-compliant agent named `information_compiler_agent`.

## Description

(TODO: Describe your agent here)

## Features

- (TODO: List key features)

## Getting Started

### Prerequisites

- Docker
- Poetry
- Python {{PYTHON_VERSION|default('3.13')}}

### Setup & Running

1.  **Navigate to this agent's directory:**
    ```bash
    cd path/to/your/agents/information_compiler_agent
    ```

2.  **Install dependencies (optional, if you want to run locally without Docker first):**
    ```bash
    poetry install
    ```

3.  **Set up environment variables:**
    Create a `.env` file in this directory if your agent requires environment variables (e.g., API keys). Refer to `information_compiler_agent/config.py` for required variables.
    Example `.env`:
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

4.  **Run with Docker (recommended for consistency):**
    Make sure you have a `docker-compose.yml` file in the parent directory (`examples/aip-agent-quickstart/`) that includes a service definition for this agent. Example:

    ```yaml
    # In examples/aip-agent-quickstart/docker-compose.yml
    services:
      information_compiler_agent:
        build:
          context: ./aip_agent_quickstart/agents/information_compiler_agent
          dockerfile: Dockerfile
        container_name: information_compiler_agent_service
        ports:
          - "8003:8003"
        restart: unless-stopped
        # environment:
        #   - OPENAI_API_KEY=${OPENAI_API_KEY}
        # volumes:
        #  - ./aip_agent_quickstart/agents/information_compiler_agent:/usr/src/app # For live dev changes
    ```

    Then, from the `examples/aip-agent-quickstart/` directory, run:
    ```bash
    docker compose up --build information_compiler_agent
    ```

5.  **Run locally (without Docker):**
    ```bash
    poetry run python -m server --port 8003
    ```

## API Endpoint

Once running, the agent will be available at `http://localhost:8003`.

-   Agent Card: `http://localhost:8003/agent-card`
-   Invoke: `http://localhost:8003/invoke` (POST request)

## Customization

-   Agent logic: Modify files in the `information_compiler_agent/` directory.
    -   `config.py`: Agent configurations, prompts, model names.
    -   `tools.py`: Define LangChain tools for your agent.
-   A2A server: Modify `server.py` for server-level or A2A-specific configurations.
-   Dependencies: Add to `pyproject.toml` and run `poetry lock && poetry install`.
