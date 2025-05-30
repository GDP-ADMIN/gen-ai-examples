"""Example of a General Assistant GoogleADKAgent that can delegate tasks to specialized agents.

This example demonstrates:
1. Configuring A2A settings for a client agent.
2. Creating a general assistant agent that can help with various queries.
3. Delegating specific tasks to specialized agents via A2A.
4. Handling responses and providing relevant advice.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.agent.types import A2AClientConfig
from gllm_agents.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)


def main():
    """Main function demonstrating the General Assistant agent with A2A capabilities."""
    agent_name = "GoogleAssistantAgent"
    assistant_agent = GoogleADKAgent(
        name=agent_name,
        instruction="You are a helpful assistant that can help with various tasks by delegating to specialized agents.",
        model="gemini-2.0-flash",
        tools=[],
        max_iterations=5,
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
    logger.info(f"Assistant Agent Response: {response['output']}")


if __name__ == "__main__":
    main()
