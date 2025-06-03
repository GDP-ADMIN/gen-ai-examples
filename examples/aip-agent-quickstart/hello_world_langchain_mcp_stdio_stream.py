"""Example showing LangChain agent with MCP tools integration and streaming capabilities using stdio transport.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.langchain_agent import LangChainAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION
from aip_agent_quickstart.mcp_configs.configs import mcp_config_stdio


async def main():
    """Demonstrates the LangChain agent with MCP tools via stdio transport and streaming."""
    langchain_agent = LangChainAgent(
        name="langchain_mcp_stream_example",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
    )
    langchain_agent.add_mcp_server(mcp_config_stdio)

    async for chunk in langchain_agent.arun_stream(query="What's the weather forecast for monday?"):
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
