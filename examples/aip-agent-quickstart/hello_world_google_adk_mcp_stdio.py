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


async def main():
    """Demonstrates the GoogleADKAgent with MCP tools via stdio transport."""
    agent_name = "ADK_Stdio_Weather_Agent_Stream"

    agent = GoogleADKAgent(
        name=agent_name,
        instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday').",
        model="gemini-2.0-flash",
    )

    agent.add_mcp_server(mcp_config_stdio)

    query = "What's the weather forecast for monday?"  # Uses MCP weather tool

    print(f"--- Agent: {agent_name} ---")
    print(f"Query: {query}")

    print("\nRunning arun with MCP stdio tools...")
    response = await agent.arun(query=query)
    print(f"Final Response: {response.get('output')}")
    print("--- End of Google ADK MCP Stdio Example ---")


if __name__ == "__main__":
    asyncio.run(main())
