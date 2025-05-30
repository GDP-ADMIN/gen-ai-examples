"""Example of a General Assistant LangChainAgent that can delegate tasks to specialized agents.

This example demonstrates:
1. Configuring A2A settings for a client agent.
2. Creating a general assistant agent that can help with various queries.
3. Delegating specific tasks to specialized agents via A2A.
4. Handling responses and providing relevant advice.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

from langchain_openai import ChatOpenAI

from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.agent.types import A2AClientConfig
from gllm_agents.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)


def main():
    """Main function demonstrating the General Assistant agent with A2A capabilities."""
    # Create the LLM
    llm = ChatOpenAI(model="gpt-4.1", temperature=0)

    # Create and return the LangChainAgent
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

    # Register agents
    assistant_agent.register_a2a_agents(agent_cards)

    query = "What is the weather in Jakarta?"
    logger.info(f"Processing Query: {query}")

    response = assistant_agent.run(query)
    final_message = response["output"]
    logger.info(f"Assistant Agent Response: {final_message}")


if __name__ == "__main__":
    main()
