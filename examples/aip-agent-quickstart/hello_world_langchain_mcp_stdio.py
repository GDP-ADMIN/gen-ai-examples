"""Example showing LangChain agent with MCP tools integration using stdio transport.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from langchain_openai import ChatOpenAI

from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.examples.mcp_configs.configs import mcp_config_stdio


async def main():
    """Demonstrates the LangChainAgent with MCP tools via stdio transport."""
    langchain_agent = LangChainAgent(
        name="langchain_mcp_example",
        instruction="""You are a helpful assistant that can provide weather forecasts.
        For weather, specify the day in lowercase (e.g., 'monday').""",
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
    )
    langchain_agent.add_mcp_server(mcp_config_stdio)

    query = "What's the weather forecast for monday?"  # Uses MCP weather tool

    print(f"\nQuery: {query}")
    response = await langchain_agent.arun(query=query)
    final_message = response["output"]
    print(f"Response: {final_message}")


if __name__ == "__main__":
    asyncio.run(main())
