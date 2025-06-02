"""Minimal LangChain agent example demonstrating asynchronous run."""

import asyncio

from gllm_agents.agent.langchain_agent import LangChainAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.tools.langchain_arithmetic_tools import add_numbers


async def main():
    """Demonstrates the LangChainAgent's arun method."""
    model = ChatOpenAI(model="gpt-4.1", temperature=0)
    tools = [add_numbers]

    langchain_agent = LangChainAgent(
        name="LangChainArithmeticAgent",
        instruction="You are a helpful assistant that can add two numbers using the add_numbers tool.",
        llm=model,
        tools=tools,
    )

    query = "What is the sum of 23 and 47? And then add 10 to that, then add 5 more."
    response = await langchain_agent.arun(
        query=query,
        configurable={"configurable": {"thread_id": "lchain_arith_example_arun"}},
    )
    print(response["output"])


if __name__ == "__main__":
    # OPENAI_API_KEY should be set in the environment.
    asyncio.run(main())
