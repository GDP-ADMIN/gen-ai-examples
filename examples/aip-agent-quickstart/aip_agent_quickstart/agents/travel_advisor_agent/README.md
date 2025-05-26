# TravelAdvisorAgent Agent

This is an A2A-compliant agent named `TravelAdvisorAgent`.

## Description

The `TravelAdvisorAgent` is designed to provide users with a list of recommended places to visit based on a specified city. It leverages a language model to understand queries and uses a dedicated tool to fetch relevant travel suggestions.

## Features

- Provides travel recommendations for various cities.
- Uses the `get_place_recommendations_tool` to fetch a list of attractions.
- Easily integrable into a multi-agent system using A2A (Agent-to-Agent) communication.
- Configurable LLM settings and agent instructions.

## Getting Started

### Prerequisites

- Docker
- Poetry
- Python {{PYTHON_VERSION|default('3.13')}}
- An OpenAI API key (if using OpenAI models)

### Setup & Running

1.  **Navigate to this agent's directory:**
    ```bash
    cd path/to/your/examples/aip-agent-quickstart/aip_agent_quickstart/agents/travel_advisor_agent
    ```

2.  **Install dependencies (optional, if you want to run locally without Docker first):**
    ```bash
    poetry install
    ```

3.  **Set up environment variables:**
    Create a `.env` file in this directory (`aip_agent_quickstart/agents/travel_advisor_agent/.env`). This is crucial for API keys and other configurations.
    Refer to `travel_advisor_agent/config.py` for required variables.
    Example `.env`:
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    # Other environment variables if needed
    ```

4.  **Run with Docker (recommended for consistency):**
    Ensure your main `docker-compose.yml` file (usually in `examples/aip-agent-quickstart/`) includes a service definition for this agent.
    Example snippet for `examples/aip-agent-quickstart/docker-compose.yml`:

    ```yaml
    services:
      travel_advisor_agent:
        build:
          context: ./aip_agent_quickstart/agents/travel_advisor_agent
          dockerfile: Dockerfile
        container_name: travel_advisor_agent_service
        ports:
          - "8002:8002" # Exposes port 8002 for the agent
        restart: unless-stopped
        environment:
          - OPENAI_API_KEY=${OPENAI_API_KEY} # Passes the API key from your host .env or shell
        # volumes:
        #  - ./aip_agent_quickstart/agents/travel_advisor_agent:/usr/src/app # Uncomment for live development changes
    ```

    Then, from the `examples/aip-agent-quickstart/` directory, run:
    ```bash
    docker compose up --build travel_advisor_agent
    ```
    To run all agents defined in your `docker-compose.yml`:
    ```bash
    docker compose up --build
    ```

5.  **Run locally (without Docker):**
    From the `examples/aip-agent-quickstart/aip_agent_quickstart/agents/travel_advisor_agent/` directory:
    ```bash
    poetry run python -m travel_advisor_agent.server --port 8002
    ```
    Ensure your `.env` file is correctly set up in this directory.

## API Endpoint

Once running, the agent will be available at `http://localhost:8002`.

-   Agent Card: `http://localhost:8002/agent-card` (GET request to get agent's metadata)
-   Invoke: `http://localhost:8002/invoke` (POST request to interact with the agent)

## Customization

-   **Agent Logic & Configuration**: Modify files in the `travel_advisor_agent/travel_advisor_agent/` directory.
    -   `config.py`: Manages agent configurations such as prompts (e.g., instructions for providing city-based place recommendations), LLM model names (like `gpt-4.1`), temperature, and API key loading.
    -   `tools.py`: Defines LangChain tools available to the agent. For this agent, it includes `get_place_recommendations_tool`, which takes a city name as input and returns a list of suggested places.
-   **A2A Server**: Modify `travel_advisor_agent/server.py` for server-level settings or A2A-specific communication protocols if needed.
-   **Dependencies**: Add any new Python package dependencies to `pyproject.toml` using `poetry add <package_name>`, then run `poetry lock && poetry install` if managing manually. Docker builds will handle this if `pyproject.toml` is updated.
