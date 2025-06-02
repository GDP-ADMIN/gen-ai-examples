"""Minimal example demonstrating the GoogleADKAgent with tool usage and async operation.

This example shows how to create a simple calculator agent using Google's ADK
which automatically handles tool calling and conversation flow.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent

from aip_agent_quickstart.config import CALCULATOR_AGENT_INSTRUCTION
from aip_agent_quickstart.tools import adk_sum_numbers

if __name__ == "__main__":
    agent = GoogleADKAgent(
        name="GoogleADKCalculator",
        instruction=CALCULATOR_AGENT_INSTRUCTION,
        model="gemini-2.0-flash",
        tools=[adk_sum_numbers],
    )

    response = agent.run(query="What is the sum of 23 and 47? And then add 10 to that, then add 5 more.")
    print(response.get("output"))
