"""Example of a General Assistant GoogleADKAgent that can delegate tasks to specialized agents.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.agent.types import A2AClientConfig

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION


async def main():
    """Main function demonstrating the General Assistant agent with streaming A2A capabilities."""
    agent = GoogleADKAgent(
        name="GoogleADKWeatherAgent",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model="gemini-2.0-flash",
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = agent.discover_agents(client_a2a_config)

    async for chunk in agent.astream_to_agent(agent_card=agent_cards[0], message="What is the weather in Jakarta?"):
        print(chunk.get("content", ""))


if __name__ == "__main__":
    asyncio.run(main())
