"""Example demonstrating a multi-agent setup with a CoordinatorAgent.

This example showcases:
1. How to define multiple specialized agents (WeatherAgent, MathAgent).
2. How to set up a CoordinatorAgent that can delegate to these specialized agents.
3. How the CoordinatorAgent uses dynamically created tools to call sub-agents.
4. How the CoordinatorAgent can delegate tasks to the appropriate sub-agents.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import (
    COORDINATOR_MULTI_AGENT_INSTRUCTION,
    MATH_AGENT_INSTRUCTION,
    WEATHER_AGENT_INSTRUCTION,
)
from aip_agent_quickstart.tools.langchain_arithmetic_tools import add_numbers
from aip_agent_quickstart.tools.langchain_weather_tool import weather_tool

if __name__ == "__main__":
    weather_agent = LangGraphAgent(
        name="WeatherAgent",
        instruction=WEATHER_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[weather_tool],
    )

    math_agent = LangGraphAgent(
        name="MathAgent",
        instruction=MATH_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[add_numbers],
    )

    coordinator_agent = LangGraphAgent(
        name="CoordinatorAgent",
        instruction=COORDINATOR_MULTI_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        agents=[weather_agent, math_agent],
    )

    response = coordinator_agent.run(query="What is the weather in Tokyo and what is 5 + 7?")
    print(response.get("output"))
