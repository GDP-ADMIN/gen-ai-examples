"""Minimal LangChain agent example demonstrating asynchronous run."""

from gllm_agents.agent.langchain_agent import LangChainAgent

from aip_agent_quickstart.config import CALCULATOR_AGENT_INSTRUCTION
from aip_agent_quickstart.tools import langchain_add_numbers

if __name__ == "__main__":
    agent = LangChainAgent(
        name="LangChainArithmeticAgent",
        instruction=CALCULATOR_AGENT_INSTRUCTION,
        model="openai-compatible/https://api.deepinfra.com/v1/openai:Qwen/Qwen3-30B-A3B",
        tools=[langchain_add_numbers],
    )

    response = agent.run(query="What is the sum of 23 and 47? And then add 10 to that, then add 5 more.")
    print(response["output"])
