"""Minimal LangGraph agent example demonstrating asynchronous run."""

import asyncio
from langchain_openai import ChatOpenAI

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from aip_agent_quickstart.tools import add_numbers


async def langgraph_example():
    """Demonstrates the LangGraphAgent's arun method."""
    model = ChatOpenAI(model="gpt-4.1", temperature=0)
    tools = [add_numbers]
    agent_name = "LangGraphArithmeticAgent"

    langgraph_agent = LangGraphAgent(
        name=agent_name,
        instruction="You are a helpful assistant that can add two numbers using the add_numbers tool.",
        model=model,
        tools=tools,
    )

    query = "What is the sum of 23 and 47? And then add 10 to that, then add 5 more."
    print(f"--- Agent: {agent_name} ---")
    print(f"Query: {query}")

    print("\nRunning arun...")
    response = await langgraph_agent.arun(
        query=query,
        configurable={"configurable": {"thread_id": "lgraph_arith_example_arun"}},
    )
    print(f"[arun] Final Response: {response}")
    print("--- End of LangGraph Example ---")


def main():
    """Run the LangGraph example."""
    asyncio.run(langgraph_example())


if __name__ == "__main__":
    main()
