"""Minimal LangGraph agent example demonstrating asynchronous run."""

import asyncio

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.tools import add_numbers


async def main():
    """Demonstrates the LangGraphAgent's arun method."""
    model = ChatOpenAI(model="gpt-4.1", temperature=0)
    tools = [add_numbers]

    langgraph_agent = LangGraphAgent(
        name="LangGraphArithmeticAgent",
        instruction="You are a helpful assistant that can add two numbers using the add_numbers tool.",
        model=model,
        tools=tools,
    )

    query = "What is the sum of 23 and 47? And then add 10 to that, then add 5 more."
    response = await langgraph_agent.arun(
        query=query,
        configurable={"configurable": {"thread_id": "lgraph_arith_example_arun"}},
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
