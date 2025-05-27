# GL AI Agents Platform - Quick Start Examples

This repository contains quick start examples demonstrating different agent implementations in the GL AI Agents Platform. Each agent follows a unified interface but uses different underlying technologies.

## Prerequisites

- Python 3.13
- Poetry (for dependency management)
- [OpenAI API key](https://platform.openai.com/api-keys) (for LangGraph example)
- [Google API key](https://ai.google.dev/) (for Google ADK example)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/GDP-ADMIN/gen-ai-examples.git
   cd gen-ai-examples/examples/aip-agent-quickstart
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

## Running Agents with MCP

### LangGraph Agent with STDIO

This example demonstrates a LangGraph-based agent that uses Model Control Protocol (MCP) over stdio for communication.

#### Start the MCP server

Open a terminal and run the following command:

```bash
poetry run python aip_agent_quickstart/mcp_servers/mcp_server_stdio.py
```

#### Setup

Open a new terminal and run the following command:

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

#### Running the Example

```bash
poetry run python hello_world_langgraph_mcp_stdio.py
```

Expected output:
```
Query: What's the weather forecast for monday?
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Response: The weather forecast for monday is sunny with temperatures between 28°C and 32°C.
```

### LangGraph Agent with SSE

This example demonstrates a LangGraph-based agent that uses Model Control Protocol (MCP) over Server-Sent Events (SSE) for communication.

#### Start the MCP server

Open a terminal and run the following command:

```bash
poetry run python aip_agent_quickstart/mcp_servers/mcp_server_sse.py
```

#### Setup

Open a new terminal and run the following command:

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

#### Running the Example

```bash
poetry run python hello_world_langgraph_mcp_sse.py
```

Expected output:
```
Query: What's the weather forecast for monday?
Response: The weather forecast for monday is sunny with temperatures between 28°C and 32°C.
```

### Google ADK Agent with STDIO

This example demonstrates a Google ADK-based agent that uses Model Control Protocol (MCP) over stdio for communication.

#### Start the MCP server

Open a terminal and run the following command:

```bash
poetry run python aip_agent_quickstart/mcp_servers/mcp_server_stdio.py
```

#### Setup

Open a new terminal and run the following command:

```bash
export GOOGLE_API_KEY='your-google-api-key-here'
```

#### Running the Example

```bash
poetry run python hello_world_google_adk_mcp_stdio.py
```

Expected output:
```
--- Agent: ADK_Stdio_Weather_Agent ---
Query: What's the weather forecast for monday?

Running arun with MCP stdio tools...

Final Response: The weather forecast for Monday is Sunny with temperatures between 28°C and 32°C.
--- End of Google ADK MCP Stdio Example ---
```

### Google ADK Agent with SSE

This example demonstrates a Google ADK-based agent that uses Model Control Protocol (MCP) over Server-Sent Events (SSE) for communication.

#### Start the MCP server

Open a terminal and run the following command:

```bash
poetry run python aip_agent_quickstart/mcp_servers/mcp_server_sse.py
```

#### Setup

Open a new terminal and run the following command:

```bash
export GOOGLE_API_KEY='your-google-api-key-here'
```

#### Running the Example

```bash
poetry run python hello_world_google_adk_mcp_sse.py
```

Expected output:
```
--- Agent: ADK_SSE_Weather_Agent ---
Query: What's the weather forecast for monday?

Running arun with MCP SSE tools...

Final Response: The weather forecast for Monday is sunny with temperatures between 28°C and 32°C.
--- End of Google ADK MCP SSE Example ---
```


### LangGraph Agent with Dockerize MCP Server

This example demonstrates how to run an MCP server in a Docker container using Docker Compose. The MCP server uses STDIO transport and will be converted to SSE transport in the Docker container using [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy).

#### Setup

1. Navigate to the `aip_agent_quickstart/mcp_server_docker` directory:
```bash
cd aip_agent_quickstart/mcp_server_docker
```

2. Start the MCP server using Docker Compose:
```bash
docker-compose up --build
```

Or run in detached mode (background):
```bash
docker-compose up -d --build
```

#### Configuration Options

You can customize the configuration using environment variables:

- **Custom port:**
```bash
HOST_PORT=9000 docker-compose up -d --build
```

#### Running the Example

Once the Docker Compose service is running, execute the client:

```bash
poetry run python hello_world_langgraph_mcp_sse.py
```

Expected output:
```
Query: What's the weather forecast for monday?
Response: The weather forecast for monday is sunny with temperatures between 28°C and 32°C.
```

## About the Examples

Both examples demonstrate the same arithmetic capabilities but use different agent implementations. They share a common interface and tooling structure, showing how different agent implementations can be used interchangeably in the GL AI Agents Platform.