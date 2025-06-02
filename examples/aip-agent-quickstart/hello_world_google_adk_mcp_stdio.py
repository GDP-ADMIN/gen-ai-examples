"""Example showing Google ADK agent with MCP tools integration using stdio transport.

This example demonstrates how to create a Google ADK agent that can use tools
from MCP servers via stdio (standard input/output) transport, which runs the
MCP server as a subprocess.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from aip_agent_quickstart.mcp_configs.configs import mcp_config_stdio

agent = GoogleADKAgent(
    name="ADK_Stdio_Weather_Agent_Stream",
    instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday').",
    model="gemini-2.0-flash",
)
agent.add_mcp_server(mcp_config_stdio)

query = "What's the weather forecast for monday?"  # Uses MCP weather tool
response = asyncio.run(agent.arun(query=query))
print(f"Response: {response.get('output')}")
