# Research Agent

A LangGraph-based agent that handles academic research queries and travel planning, delegating to specialized services and agents when appropriate.

## Capabilities

The Research Agent can:

1. **Academic Research**: Using Arxiv MCP tools, it can search for academic papers, filter by keywords/authors/topics, and summarize research trends.
2. **Travel Planning**: Delegate travel-related queries to specialized agents (Web Search Agent & Information Compiler Agent) when available.
3. **Topic Classification**: Automatically classify queries to determine the appropriate service to use.

## Prerequisites

- Python 3.13
- Poetry (for dependency management)
- OpenAI API Key
- VPN connection for accessing the Arxiv MCP server (http://mcp.obrol.id:8006)

## Installation

```bash
cd aip_agent_quickstart/agents/research_agent
poetry install
```

## Running the Agent

### Local Development

```bash
# Set your OpenAI API key
export OPENAI_API_KEY='your-openai-api-key'

# Run the agent server
python server.py
```

### Using Podman

```bash
# Build the image
podman build -t research_agent .

# Run the container
podman run -p 8002:8002 -e OPENAI_API_KEY='your-openai-api-key' research_agent
```

The agent will be accessible at http://localhost:8002

## Sample Queries

### Academic Research

- "Find recent papers about quantum computing in cryptography"
- "Summarize research trends in transformer models from 2023-2025"
- "Search for papers by Geoffrey Hinton about neural networks"

### Travel Planning

- "Plan a 3-day trip to Bali with budget considerations"
- "What are popular tourist spots in Tokyo?"
- "Find the best time to visit Paris and typical weather conditions"

## Integration with Main Project

To include the Research Agent in the main docker-compose.yml file, add the following configuration:

```yaml
services:
  research_agent:
    build:
      context: ./aip_agent_quickstart/agents/research_agent
    ports:
      - "8002:8002"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## Notes

- The Research Agent requires access to the Arxiv MCP server, which may need a VPN connection
- The server exposes an A2A interface at port 8002, allowing it to be used by other agents
- For academic queries, the agent uses the Arxiv tools from the MCP server
- For travel queries, the agent will delegate to other specialized agents when available
