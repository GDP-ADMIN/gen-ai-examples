"""Example of a General Assistant LangChainAgent that can delegate tasks to specialized agents.

This example demonstrates:
1. Configuring A2A settings for a client agent.
2. Creating a general assistant agent that can help with various queries.
3. Delegating specific tasks to specialized agents via A2A with streaming.
4. Handling streaming responses and providing relevant advice.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

import asyncio

from a2a.types import TaskState
from langchain_openai import ChatOpenAI

from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.agent.types import A2AClientConfig
from gllm_agents.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)


async def main():
    """Main function demonstrating the General Assistant agent with streaming A2A capabilities."""
    llm = ChatOpenAI(model="gpt-4.1", streaming=True)

    assistant_agent = LangChainAgent(
        name="AssistantAgentLangChain",
        instruction="""You are a helpful assistant that can help with various tasks
        by delegating to specialized agents.""",
        llm=llm,
        tools=[],
    )

    # Discover agents
    client_a2a_config = A2AClientConfig(
        discovery_urls=["http://localhost:8001"],
    )
    agent_cards = assistant_agent.discover_agents(client_a2a_config)

    query = "What is the weather in Jakarta?"
    logger.info(f"Processing Query: {query}")

    agent_result = ""
    async for chunk in assistant_agent.astream_to_agent(
        agent_card=agent_cards[0], message=query
    ):
        task_state = chunk.get("task_state")
        content = chunk.get("content", "")
        if task_state == str(TaskState.working) and content:
            logger.info(f"Event Working: {content}")
        elif task_state == str(TaskState.completed) and content:
            agent_result += content

    logger.info(f"Agent Response: {agent_result}")
    return agent_result


if __name__ == "__main__":
    asyncio.run(main())
