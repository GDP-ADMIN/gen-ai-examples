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
    """Demonstrates the GoogleADKAgent with MCP tools via stdio transport and streaming."""
    agent_name = "GoogleADKMCPStdioStream"

    # Create the agent with simplified instructions for weather forecasting
    agent = GoogleADKAgent(
        name=agent_name,
        instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday'). Explain your steps clearly for streaming demonstration.",
        model="gemini-2.0-flash",
        tools=[],  # Start with no tools, will add MCP tools
        max_iterations=5,
    )

    # Add the MCP server with stdio transport
    agent.add_mcp_server(mcp_config_stdio)

    query = "What's the weather forecast for monday?"  # Uses MCP weather tool

    print(f"--- Agent: {agent_name} ---")
    print(f"Query: {query}")

    print("\nRunning arun_stream with MCP stdio tools...")
    print("Streaming response:")

    # Stream the response chunks
    async for chunk in agent.arun_stream(query=query):
        print(chunk, end="", flush=True)

    print("\n--- End of Google ADK MCP Stdio Streaming Example ---")


if __name__ == "__main__":
    # GOOGLE_API_KEY should be set in the environment.
    # The MCP server will be started automatically as a subprocess
    asyncio.run(main())
