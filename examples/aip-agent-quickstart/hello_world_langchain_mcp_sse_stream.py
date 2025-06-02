"""Example showing LangChain agent with MCP tools integration and streaming capabilities using SSE transport.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from langchain_openai import ChatOpenAI

from gllm_agents.agent.langchain_agent import LangChainAgent
from aip_agent_quickstart.mcp_configs.configs import mcp_config_sse


async def main():
    langchain_agent = LangChainAgent(
        name="langchain_mcp_stream_example",
        instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday').",
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
    )
    langchain_agent.add_mcp_server(mcp_config_sse)

    async for chunk in langchain_agent.arun_stream(
        query="What's the weather forecast for monday?"
    ):
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
