"""Minimal LangChain agent example demonstrating asynchronous run."""

from gllm_agents.agent.langchain_agent import LangChainAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.tools.langchain_arithmetic_tools import add_numbers

if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-4.1", temperature=0)

    langchain_agent = LangChainAgent(
        name="LangChainArithmeticAgent",
        instruction="You are a helpful assistant that can add two numbers using the add_numbers tool.",
        llm=model,
        tools=[add_numbers],
    )

    query = "What is the sum of 23 and 47? And then add 10 to that, then add 5 more."
    response = langchain_agent.run(query=query)
    print(response["output"])
