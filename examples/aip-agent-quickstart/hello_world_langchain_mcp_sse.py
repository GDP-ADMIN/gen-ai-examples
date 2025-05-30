"""Example showing LangChain agent with MCP tools integration using SSE transport.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from langchain.agents import AgentType
from langchain_openai import ChatOpenAI

from gllm_agents.agent.langchain_agent import LangChainAgent
from aip_agent_quickstart.mcp_configs.configs import mcp_config_sse


async def main():
    """Demonstrates the LangChainAgent with MCP tools via SSE transport."""
    langchain_agent = LangChainAgent(
        name="langchain_mcp_example",
        instruction="""You are a helpful assistant that can provide weather forecasts.
        For weather, specify the day in lowercase (e.g., 'monday').""",
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
        agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    )
    langchain_agent.add_mcp_server(mcp_config_sse)

    query = "What's the weather forecast for monday?"  # Uses MCP weather tool

    print(f"\nQuery: {query}")
    response = await langchain_agent.arun(query=query)
    # Get the final response from output.messages
    final_message = response["output"]
    print(f"Response: {final_message}")


if __name__ == "__main__":
    asyncio.run(main())
