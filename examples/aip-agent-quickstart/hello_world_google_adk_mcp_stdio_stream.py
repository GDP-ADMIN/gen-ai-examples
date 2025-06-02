"""Example showing Google ADK agent with MCP tools integration using stdio transport and streaming capabilities.

This example demonstrates how to create a Google ADK agent that can use tools
from MCP servers via stdio (standard input/output) transport while streaming the response
in real-time. The MCP server runs as a subprocess.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from aip_agent_quickstart.mcp_configs.configs import mcp_config_stdio


async def main():
    agent = GoogleADKAgent(
        name="ADK_Stdio_Weather_Agent",
        instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday'). Explain your steps clearly for streaming demonstration.",
        model="gemini-2.0-flash",
    )
    agent.add_mcp_server(mcp_config_stdio)

    query = "What's the weather forecast for monday?"  # Uses MCP weather tool
    async for chunk in agent.arun_stream(query=query):
        print(chunk, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
