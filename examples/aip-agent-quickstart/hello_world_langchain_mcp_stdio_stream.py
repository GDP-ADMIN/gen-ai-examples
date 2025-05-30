"""Example showing LangChain agent with MCP tools integration and streaming capabilities using stdio transport.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from langchain_openai import ChatOpenAI

from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.examples.mcp_configs.configs import mcp_config_stdio


async def main():
    """Demonstrates the LangChainAgent with MCP tools via stdio transport and streaming capabilities."""
    langchain_agent = LangChainAgent(
        name="langchain_mcp_stream_example",
        instruction="""You are a helpful assistant that can provide weather forecasts.
        For weather, specify the day in lowercase (e.g., 'monday').""",
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
    )
    langchain_agent.add_mcp_server(mcp_config_stdio)

    query = "What's the weather forecast for monday?"  # Uses MCP weather tool

    stream_thread_id = "langchain_mcp_stream_example"

    print(f"\nQuery: {query}")
    print("Streaming response:")

    full_response = ""
    async for chunk in langchain_agent.arun_stream(
        query=query, configurable={"configurable": {"thread_id": stream_thread_id}}
    ):
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)
            full_response += chunk
        elif isinstance(chunk, dict) and "messages" in chunk:
            print("\n(Stream finished with final state object)")
        elif isinstance(chunk, dict):
            pass

    print(f"\nFull response collected: {full_response}")


if __name__ == "__main__":
    asyncio.run(main())
