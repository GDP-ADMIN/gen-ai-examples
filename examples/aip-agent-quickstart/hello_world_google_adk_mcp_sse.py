"""Example showing Google ADK agent with MCP tools integration using SSE transport.

This example demonstrates how to create a Google ADK agent that can use tools
from MCP servers via Server-Sent Events (SSE) transport.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.examples.mcp_configs.configs import mcp_config_sse

agent = GoogleADKAgent(
    name="ADK_SSE_Weather_Agent",
    instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday').",
    model="gemini-2.0-flash",
)
agent.add_mcp_server(mcp_config_sse)

query = "What's the weather forecast for monday?"  # Uses MCP weather tool
response = asyncio.run(agent.arun(query=query))
print(f"Response: {response.get('output')}")
