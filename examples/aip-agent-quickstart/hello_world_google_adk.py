"""Minimal example demonstrating the GoogleADKAgent with tool usage and async operation.

This example shows how to create a simple calculator agent using Google's ADK
which automatically handles tool calling and conversation flow.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent

from aip_agent_quickstart.tools.adk_arithmetic_tools import sum_numbers

if __name__ == "__main__":
    agent = GoogleADKAgent(
        name="GoogleADKCalculator",
        instruction=(
            "You are a calculator assistant. When asked math problems, extract numbers and call sum_numbers tool "
            "to add them. For multi-step problems, use multiple tool calls."
        ),
        model="gemini-2.0-flash",
        tools=[sum_numbers],
    )

    response = agent.run(query="What is the sum of 23 and 47? And then add 10 to that, then add 5 more.")
    print(response.get("output"))
