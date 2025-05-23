"""Example showing Google ADK agent with MCP tools integration using SSE transport.

This example demonstrates how to create a Google ADK agent that can use tools
from MCP servers via Server-Sent Events (SSE) transport.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.examples.mcp_configs.configs import mcp_config_sse


async def main():
    """Demonstrates the GoogleADKAgent with MCP tools via SSE transport."""
    agent_name = "GoogleADKMCPSSE"

    # Create the agent with simplified instructions for weather forecasting
    agent = GoogleADKAgent(
        name=agent_name,
        instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday').",
        model="gemini-2.0-flash",
        tools=[],  # Start with no tools, will add MCP tools
        max_iterations=5,
    )

    # Add the MCP server with SSE transport
    agent.add_mcp_server(mcp_config_sse)

    query = "What's the weather forecast for monday?"  # Uses MCP weather tool

    print(f"--- Agent: {agent_name} ---")
    print(f"Query: {query}")

    print("\nRunning arun with MCP SSE tools...")
    response = await agent.arun(query=query)
    print(f"[arun] Final Response: {response.get('output')}")
    print("--- End of Google ADK MCP SSE Example ---")


if __name__ == "__main__":
    # GOOGLE_API_KEY should be set in the environment.
    # Make sure the MCP SSE server is running on http://localhost:8000/sse
    asyncio.run(main())
