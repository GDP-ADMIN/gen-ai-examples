"""Example showing LangGraph agent with MCP tools integration.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

import asyncio

from langchain_openai import ChatOpenAI
from gllm_agents.agent.langgraph_agent import LangGraphAgent
from aip_agent_quickstart.mcp_configs.configs import mcp_config_sse

async def main():
    langgraph_agent = LangGraphAgent(
        name="langgraph_mcp_example",
        instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday').",
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
    )
    langgraph_agent.add_mcp_server(mcp_config_sse)

    query = "What's the weather forecast for monday?"  # Uses MCP weather tool

    print(f"\nQuery: {query}")
    response = await langgraph_agent.arun(query=query)
    print(f"Response: {response['output']}")


if __name__ == "__main__":
    asyncio.run(main())
