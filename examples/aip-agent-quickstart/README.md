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
## Running the Examples

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

## About the Examples

Both examples demonstrate the same arithmetic capabilities but use different agent implementations. They share a common interface and tooling structure, showing how different agent implementations can be used interchangeably in the GL AI Agents Platform.