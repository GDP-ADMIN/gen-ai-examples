"""Minimal LangChain agent example demonstrating streaming capabilities.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.langchain_agent import LangChainAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.tools.langchain_arithmetic_tools import add_numbers


async def main():
    """Demonstrates the LangChainAgent's arun_stream method with async execution."""
    agent = LangChainAgent(
        name="LangChainStreamingCalculator",
        instruction=(
            "You are a helpful calculator assistant that can add numbers. "
            "When asked to add numbers, use the add_numbers tool. "
            "Explain your steps clearly for streaming demonstration."
        ),
        llm=ChatOpenAI(model="gpt-4.1", streaming=True),
        tools=[add_numbers],
        verbose=False,
    )

    query = "What is the sum of 23 and 47? And then add 10 to that, then add 5 more."
    async for chunk in agent.arun_stream(query=query):
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
