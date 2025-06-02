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

from aip_agent_quickstart.tools.langchain_arithmetic_tools import add_numbers
from aip_agent_quickstart.tools.langchain_weather_tool import weather_tool

if __name__ == "__main__":
    weather_agent = LangGraphAgent(
        name="WeatherAgent",
        instruction="You are a weather expert. You must use the get_weather tool to find weather information.",
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[weather_tool],
    )

    math_agent = LangGraphAgent(
        name="MathAgent",
        instruction=(
            "You are a math expert. You must use the 'add_numbers' tool to perform addition. "
            "The tool takes two integer arguments: 'a' and 'b'. For example, to add 5 and 7, "
            "you would call add_numbers(a=5, b=7)."
        ),
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[add_numbers],
    )

    coordinator_agent = LangGraphAgent(
        name="CoordinatorAgent",
        instruction=(
            "You are a coordinator agent. Your primary role is to delegate tasks to specialized agents. "
            "Based on the user's query, decide which agent (WeatherAgent or MathAgent) is best suited. "
            "If a query involves multiple aspects, delegate accordingly. Synthesize their responses."
        ),
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        agents=[weather_agent, math_agent],
    )

    query = "What is the weather in Tokyo and what is 5 + 7?"
    response = coordinator_agent.run(query=query)
    print(response.get("output"))
