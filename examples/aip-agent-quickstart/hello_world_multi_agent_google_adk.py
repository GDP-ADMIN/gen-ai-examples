"""Multi-agent example using Google ADK with a coordinator agent.

This example demonstrates a coordinator agent that can delegate tasks to specialized agents.
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent

from aip_agent_quickstart.config import (
    COORDINATOR_MULTI_AGENT_INSTRUCTION,
    MATH_AGENT_INSTRUCTION,
    WEATHER_AGENT_INSTRUCTION,
)
from aip_agent_quickstart.tools import adk_sum_numbers, adk_weather_tool

if __name__ == "__main__":
    weather_agent = GoogleADKAgent(
        name="WeatherAgent",
        instruction=WEATHER_AGENT_INSTRUCTION,
        model="gemini-2.0-flash",
        tools=[adk_weather_tool],
    )

    math_agent = GoogleADKAgent(
        name="MathAgent",
        instruction=MATH_AGENT_INSTRUCTION,
        model="gemini-2.0-flash",
        tools=[adk_sum_numbers],
    )

    coordinator_agent = GoogleADKAgent(
        name="CoordinatorAgent",
        instruction=COORDINATOR_MULTI_AGENT_INSTRUCTION,
        model="gemini-2.0-flash",
        agents=[weather_agent, math_agent],
    )

    weather_response = coordinator_agent.run(query="What is the weather in Tokyo?")
    math_response = coordinator_agent.run(query="What is 5 + 7?")

    print(f"Weather Response: {weather_response.get('output')}\nMath Response: {math_response.get('output')}")
