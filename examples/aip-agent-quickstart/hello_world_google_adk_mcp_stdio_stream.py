"""Example showing Google ADK agent with MCP tools integration using stdio transport and streaming capabilities.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.google_adk_agent import GoogleADKAgent

from aip_agent_quickstart.mcp_configs.configs import mcp_config_stdio


async def main():
    """Demonstrates the GoogleADK agent with MCP tools via stdio transport and streaming."""
    agent = GoogleADKAgent(
        name="ADK_Stdio_Weather_Agent",
        instruction="You are a helpful assistant that can provide weather forecasts.",
        model="gemini-2.0-flash",
    )
    agent.add_mcp_server(mcp_config_stdio)

    async for chunk in agent.arun_stream(query="What's the weather forecast for monday?"):
        print(chunk, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
