"""Minimal LangGraph agent example demonstrating asynchronous run."""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.tools import add_numbers

if __name__ == "__main__":
    agent = LangGraphAgent(
        name="LangGraphArithmeticAgent",
        instruction="You are a helpful assistant that can add two numbers using the add_numbers tool.",
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[add_numbers],
    )

    response = agent.run(query="What is the sum of 23 and 47? And then add 10 to that, then add 5 more.")
    print(response["output"])
