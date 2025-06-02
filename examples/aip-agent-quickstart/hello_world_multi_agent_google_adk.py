"""Multi-agent example using Google ADK with a coordinator agent.

This example demonstrates a coordinator agent that can delegate tasks to specialized agents.
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent

from aip_agent_quickstart.tools.adk_arithmetic_tools import sum_numbers
from aip_agent_quickstart.tools.adk_weather_tool import get_weather

if __name__ == "__main__":
    weather_agent = GoogleADKAgent(
        name="WeatherAgent",
        instruction=(
            "You are a weather expert. You must use the weather_tool "
            "to find weather information for a given city. "
            "Always include the city name in your response."
        ),
        model="gemini-2.0-flash",
        tools=[get_weather],
    )

    math_agent = GoogleADKAgent(
        name="MathAgent",
        instruction=(
            "You are a math expert. You must use the sum_numbers tool to perform addition. "
            "The tool takes two integer arguments: 'a' and 'b'. "
            "For example, to add 5 and 7, you would call sum_numbers(a=5, b=7). "
            "Always state the numbers you're adding in your response."
        ),
        model="gemini-2.0-flash",
        tools=[sum_numbers],
    )

    coordinator_agent = GoogleADKAgent(
        name="CoordinatorAgent",
        instruction=(
            "You are a helpful assistant that coordinates between specialized agents.\n"
            "When asked about weather, delegate to WeatherAgent.\n"
            "When asked to do math, delegate to MathAgent.\n"
            "If asked multiple questions, break them down and handle each one separately.\n"
            "Always be concise and helpful in your responses."
        ),
        model="gemini-2.0-flash",
        agents=[weather_agent, math_agent],
    )

    weather_response = coordinator_agent.run(query="What is the weather in Tokyo?")
    math_response = coordinator_agent.run(query="What is 5 + 7?")

    print(f"Weather Response: {weather_response.get('output')}\nMath Response: {math_response.get('output')}")
