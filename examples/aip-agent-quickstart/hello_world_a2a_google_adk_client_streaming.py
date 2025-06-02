"""Example of a General Assistant GoogleADKAgent that can delegate tasks to specialized agents.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

import asyncio

from a2a.types import TaskState
from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.agent.types import A2AClientConfig


async def main():
    """Main function demonstrating the General Assistant agent with streaming A2A capabilities."""
    assistant_agent = GoogleADKAgent(
        name="GoogleADKWeatherAgent",
        instruction="You are a helpful assistant that can help with various tasks by delegating to specialized agents.",
        model="gemini-2.0-flash",
        tools=[],
        max_iterations=5,
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = assistant_agent.discover_agents(client_a2a_config)

    query = "What is the weather in Jakarta?"
    agent_result = ""

    async for chunk in assistant_agent.astream_to_agent(agent_card=agent_cards[0], message=query):
        task_state = chunk.get("task_state")
        content = chunk.get("content", "")
        if task_state == str(TaskState.completed) and content:
            agent_result += content

    print(agent_result)


if __name__ == "__main__":
    asyncio.run(main())
