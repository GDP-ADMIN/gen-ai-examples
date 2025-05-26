"""Example client script to interact with WeatherAgent and TravelAdvisorAgent running in Docker.

This script demonstrates:
1. Setting up a LangGraphAgent as a client.
2. Discovering and registering multiple agents (WeatherAgent and TravelAdvisorAgent).
3. Sending a query that requires capabilities from both registered agents.
4. Printing the consolidated response.
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.agent.types import A2AClientConfig
from gllm_agents.utils.logger_manager import LoggerManager
from langchain_openai import ChatOpenAI

logger = LoggerManager().get_logger(__name__)


def main() -> None:
    """Runs the A2A client to interact with Weather and Travel Advisor agents."""
    llm = ChatOpenAI(model="gpt-4.1", temperature=0)

    client_agent = LangGraphAgent(
        name="DockerDemoClientAgent",
        instruction=(
            "You are a helpful assistant. Your task is to understand the user's query "
            "and delegate tasks to specialized agents to get the necessary information. "
            "Combine the information from the agents into a coherent response."
        ),
        model=llm,
        tools=[],
    )
    client_a2a_config = A2AClientConfig(
        discovery_urls=["http://localhost:8001", "http://localhost:8002"],
    )

    logger.info(f"Attempting to discover agents at: {client_a2a_config.discovery_urls}")
    agent_cards = client_agent.discover_agents(client_a2a_config)

    if not agent_cards:
        logger.error(
            "No agents discovered. Ensure the WeatherAgent and TravelAdvisorAgent are running."
        )
        return

    logger.info(
        f"Discovered {len(agent_cards)} agent(s): {[card.name for card in agent_cards]}"
    )

    client_agent.register_a2a_agents(agent_cards)
    logger.info("Registered agents with the client.")

    query = "What is the weather in Paris and can you recommend some historical places to visit there?"
    logger.info(f"Processing Query: {query}")

    response = client_agent.run(query)

    logger.info(f"Agent Response:\n{response['output']}")


if __name__ == "__main__":
    main()
