"""Example of a General Assistant LangChainAgent that can delegate tasks to specialized agents.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.agent.types import A2AClientConfig
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION


async def main():
    """Demonstrates LangChainAgent with streaming A2A capabilities."""
    agent = LangChainAgent(
        name="AssistantAgentLangChain",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", streaming=True),
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = agent.discover_agents(client_a2a_config)

    async for chunk in agent.astream_to_agent(agent_card=agent_cards[0], message="What is the weather in Jakarta?"):
        print(chunk.get("content", ""))


if __name__ == "__main__":
    asyncio.run(main())
