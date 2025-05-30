"""Minimal LangChain agent example demonstrating streaming capabilities.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)

"""

import asyncio

from langchain_openai import ChatOpenAI

from gllm_agents.agent.langchain_agent import LangChainAgent
from aip_agent_quickstart.tools.langchain_arithmetic_tools import add_numbers


async def langchain_stream_example():
    """Demonstrates the LangChainAgent's arun_stream method with async execution."""
    # Initialize the language model
    model = ChatOpenAI(model="gpt-4.1", temperature=0)

    tools = [add_numbers]
    agent_name = "LangChainStreamingCalculator"

    # Create the LangChain agent
    agent = LangChainAgent(
        name=agent_name,
        instruction="You are a helpful calculator assistant that can add numbers. "
        "When asked to add numbers, use the add_numbers tool. "
        "Explain your steps clearly for streaming demonstration.",
        llm=model,
        tools=tools,
        verbose=False,
    )

    # Define the query
    query = "What is the sum of 23 and 47? And then add 10 to that, then add 5 more."
    print(f"--- Agent: {agent_name} ---")
    print(f"Query: {query}")

    print("\nRunning arun_stream...")
    print("Streaming response:")

    # Stream the response chunks
    async for chunk in agent.arun_stream(query=query):
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)  # Print text chunks as they come in

    print("\n\n--- End of LangChain Streaming Example ---")


if __name__ == "__main__":
    # OPENAI_API_KEY should be set in the environment
    asyncio.run(langchain_stream_example())
