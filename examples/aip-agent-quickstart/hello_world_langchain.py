"""Minimal LangChain agent example demonstrating asynchronous run."""

import asyncio

from langchain_openai import ChatOpenAI

from gllm_agents.agent.langchain_agent import LangChainAgent
from aip_agent_quickstart.tools.langchain_arithmetic_tools import add_numbers


async def langchain_example():
    """Demonstrates the LangChainAgent's arun method."""
    model = ChatOpenAI(model="gpt-4.1", temperature=0)

    tools = [add_numbers]

    agent_name = "LangChainArithmeticAgent"

    langchain_agent = LangChainAgent(
        name=agent_name,
        instruction="You are a helpful assistant that can add two numbers using the add_numbers tool.",
        llm=model,
        tools=tools,
    )

    query = "What is the sum of 23 and 47? And then add 10 to that, then add 5 more."
    print(f"--- Agent: {agent_name} ---")
    print(f"Query: {query}")

    print("\nRunning arun...")
    response = await langchain_agent.arun(
        query=query,
        configurable={"configurable": {"thread_id": "lchain_arith_example_arun"}},
    )
    final_message = response["output"]
    print(f"[arun] Final Response: {final_message}")
    print("--- End of LangChain Example ---")


if __name__ == "__main__":
    # OPENAI_API_KEY should be set in the environment.
    asyncio.run(langchain_example())
