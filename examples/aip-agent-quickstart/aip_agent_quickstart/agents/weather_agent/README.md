# Weather Agent

A simple A2A weather agent built with LangGraph.

## Overview

This agent provides weather information for cities using a mock weather database. It demonstrates how to set up an A2A-compatible agent using the LangGraph framework.

## Project Structure

```
weather_agent/
├── Dockerfile             # Docker configuration for containerization
├── docker-compose.yml     # Docker Compose configuration
├── weather_agent/         # Actual agent code
│   ├── __init__.py
│   ├── config.py
├── __init__.py
├── server.py
└── README.md
```

## Usage

### Running Locally

Run the agent server:

```bash
python -m aip_agent_quickstart.agents.weather_agent.server --host localhost --port 8001
```

The agent will be available at http://localhost:8001.

### Running with Docker

There are two ways to run the agent with Docker:

#### 1. Using Docker Compose (Recommended for Production)

```bash
# From the weather_agent directory
# Create a .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env
# Start the container
docker-compose up -d
```

#### 2. Using Docker directly

```bash
# From the project root
# Build the image
docker build -f examples/aip-agent-quickstart/aip_agent_quickstart/agents/weather_agent/Dockerfile -t weather-agent .
# Run the container
docker run -d -p 8001:8001 -e OPENAI_API_KEY=your_key_here weather-agent
```

## Technical Details

### Dependencies

This agent relies on:
- LangGraph for agent creation
- A2A types for protocol compatibility
- LangChain OpenAI for LLM integration
- The weather_tool from tools package

### Containerization

The Dockerfile:
- Uses Python 3.13 slim image
- Employs Poetry for dependency management
- Only copies the necessary weather_agent code and weather_tool
- Creates a proper module structure for imports
- Runs as a non-root user for security
- Uses a multi-stage build for efficiency

## Examples

Try asking the agent:
- "What's the weather in Tokyo?"
- "Get weather for London"
- "How's the weather in Singapore today?"
