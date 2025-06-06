"""Example showing LangGraph agent with MCP tools integration and streaming capabilities.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION
from aip_agent_quickstart.mcp_configs.configs import mcp_config_sse


async def main():
    """Demonstrates the LangGraph agent with MCP tools via SSE transport and streaming."""
    langgraph_agent = LangGraphAgent(
        name="langgraph_mcp_stream_example",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
    )
    langgraph_agent.add_mcp_server(mcp_config_sse)

    async for chunk in langgraph_agent.arun_stream(query="What's the weather forecast for monday?"):
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
