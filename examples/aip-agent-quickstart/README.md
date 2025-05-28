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

### LangGraph Agent with Dockerize ArXiv MCP Server

This example demonstrates how to run an [ArXiv MCP server](https://github.com/blazickjp/arxiv-mcp-server) in a Podman container using `podman-compose`. The ArXiv MCP server uses STDIO transport and will be converted to SSE transport in the Podman container using [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy).

#### Setup

Build Podman image:
```bash
podman-compose --build arxiv_mcp_server
```

Start the MCP server:
```bash
podman-compose up arxiv_mcp_server
```

Or run in detached mode (background):
```bash
podman-compose up -d arxiv_mcp_server
```

#### Running the Example

Once the MCP server service is running, execute the client:

```bash
poetry run python hello_world_arxiv_langgraph_mcp_sse.py
```

Expected output:
```
Query: Search for research papers about transformer large language models (LLMs) published between January 2025 and May 2025. Focus on papers that discuss Transformer architectures and improvements

Response: Here are recent research papers (Jan–May 2025) related to Transformer large language models (LLMs), focusing on architecture and improvements:

1. **Hard Negative Contrastive Learning for Fine-Grained Geometric Understanding in Large Multimodal Models**
   - **Authors:** Kai Sun, Yushi Bai, Zhen Yang, Jiajie Zhang, Ji Qi, Lei Hou, Juanzi Li
   - **Abstract:** Proposes a novel hard negative contrastive learning framework for vision encoders in large multimodal models (LMMs), enhancing geometric reasoning. The method, MMGeoLM, outperforms other open-source models and rivals GPT-4o in geometric tasks. The study also analyzes the impact of negative sample construction on LMM performance.
   - **arXiv ID:** 2505.20152v1
   - [Read PDF](http://arxiv.org/pdf/2505.20152v1)

2. **On the (Non) Injectivity of Piecewise Linear Janossy Pooling**
   - **Authors:** Ilai Reshef, Nadav Dym
   - **Abstract:** Investigates multiset functions in neural networks, relevant for Transformer architectures. The paper proves that no piecewise linear Janossy pooling function can be injective, impacting the design of efficient and expressive pooling mechanisms in LLMs and graph neural networks.
   - **arXiv ID:** 2505.20150v1
   - [Read PDF](http://arxiv.org/pdf/2505.20150v1)

While other papers in the search results focus on statistical methods, entropy estimation, or medical imaging, the two above are most relevant to Transformer LLM architectures and their improvements. If you want more details or a deeper dive into any of these papers, let me know!
```

## About the Examples

Both examples demonstrate the same arithmetic capabilities but use different agent implementations. They share a common interface and tooling structure, showing how different agent implementations can be used interchangeably in the GL AI Agents Platform.