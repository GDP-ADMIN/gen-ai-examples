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

## Running Agents

### LangGraph Agent

This example demonstrates a LangGraph-based agent that can perform arithmetic operations using OpenAI's GPT models.

#### Setup

Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

#### Running the Example

```bash
poetry run python hello_world_langgraph_agent.py
```

Expected output:
```
--- Agent: LangGraphArithmeticAgent ---
Query: What is the sum of 23 and 47? And then add 10 to that, then add 5 more.
Running arun...
[arun] Final Response: {'output': 'The sum of 23 and 47 is 70. Adding 10 to that gives 80, and adding 5 more gives a final result of 85.', 'full_final_state': {...}}
--- End of LangGraph Example ---
```

### LangGraph Agent with BOSA

This example demonstrates a LangGraph-based agent that can perform Twitter user details retrieval using BOSA.

#### Setup

Set your BOSA API key:
```bash
export BOSA_API_BASE_URL="your-bosa-api-base-url-here"
export BOSA_API_KEY='your-bosa-api-key-here'
```

#### Running the Example

```bash
poetry run python hello_world_langgraph_bosa_twitter.py
```

Expected output:
```
--- Agent: LangGraphBosaTwitterAgent ---
Query: Get me user details for Twitter user @elonmusk

Running arun...
[arun] Final Response: {'output': 'Here are the details for the Twitter user @elonmusk:\n\n- Name: Elon Musk\n- Username: elonmusk\n- User ID: 44196397\n\nIf you need more specific information or recent tweets, let me know!', 'full_final_state': {...}}
--- End of LangGraph Example ---
```

### Google ADK Agent

This example demonstrates a Google ADK-based agent that can perform arithmetic operations using Google's AI models.

#### Setup

Set your Google API key:
```bash
export GOOGLE_API_KEY='your-google-api-key-here'
```

#### Running the Example

```bash
poetry run python hello_world_google_adk.py
```

Expected output:
```
--- Agent: GoogleADKCalculator ---
Query: What is the sum of 23 and 47? And then add 10 to that, then add 5 more.
Running arun...
Tool executed: sum_numbers(23, 47)
Tool executed: sum_numbers(70, 10)
Tool executed: sum_numbers(80, 5)
[arun] Final Response: The sum of 23 and 47 is 70. Adding 10 to that gives 80, and adding 5 more results in 85.
--- End of Google ADK Example ---
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

This example demonstrates how to run an MCP server in a Podman container using `podman-compose`. The MCP server uses STDIO transport and will be converted to SSE transport in the Podman container using [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy).

#### Setup

Build Podman image:
```bash
podman-compose --build
```

Start the MCP server using `podman-compose`:
```bash
podman-compose up weather_mcp_server
```

Or run in detached mode (background):
```bash
podman-compose up -d weather_mcp_server
```

#### Running the Example

Once the MCP server service is running, execute the client:

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