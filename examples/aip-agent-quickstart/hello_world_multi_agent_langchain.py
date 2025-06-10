"""Example demonstrating a multi-agent setup with a CoordinatorAgent.

This example showcases:
1. How to define multiple specialized agents (WeatherAgent, MathAgent).
2. How to set up a CoordinatorAgent that can delegate to these specialized agents.
3. How the CoordinatorAgent uses dynamically created tools to call sub-agents.
4. How the CoordinatorAgent can delegate tasks to the appropriate sub-agents.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

from gllm_agents.agent.langchain_agent import LangChainAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import (
    COORDINATOR_MULTI_AGENT_INSTRUCTION,
    MATH_AGENT_INSTRUCTION,
    WEATHER_AGENT_INSTRUCTION,
)
from aip_agent_quickstart.tools import langchain_add_numbers, langchain_weather_tool

if __name__ == "__main__":
    weather_agent = LangChainAgent(
        name="WeatherAgent",
        instruction=WEATHER_AGENT_INSTRUCTION,
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[langchain_weather_tool],
    )

    math_agent = LangChainAgent(
        name="MathAgent",
        instruction=MATH_AGENT_INSTRUCTION,
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[langchain_add_numbers],
    )

    coordinator_agent = LangChainAgent(
        name="CoordinatorAgent",
        instruction=COORDINATOR_MULTI_AGENT_INSTRUCTION,
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        agents=[weather_agent, math_agent],
    )

    response = coordinator_agent.run(query="What is the weather in Tokyo and what is 5 + 7?")
    print(response.get("output"))
