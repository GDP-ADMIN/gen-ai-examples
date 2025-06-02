"""Example of a General Assistant LangChainAgent that can delegate tasks to specialized agents.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from a2a.types import TaskState
from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.agent.types import A2AClientConfig
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION


async def main():
    """Demonstrates LangChainAgent with streaming A2A capabilities."""
    agent = LangChainAgent(
        name="AssistantAgentLangChain",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        llm=ChatOpenAI(model="gpt-4.1", streaming=True),
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = agent.discover_agents(client_a2a_config)

    agent_result = ""
    async for chunk in agent.astream_to_agent(agent_card=agent_cards[0], message="What is the weather in Jakarta?"):
        task_state = chunk.get("task_state")
        content = chunk.get("content", "")
        if task_state == str(TaskState.working) and content:
            agent_result += f"Event Working: {content}\n"
        if task_state == str(TaskState.completed) and content:
            agent_result += content

    print(agent_result)


if __name__ == "__main__":
    asyncio.run(main())
