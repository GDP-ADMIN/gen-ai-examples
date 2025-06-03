"""Example of a General Assistant GoogleADKAgent that can delegate tasks to specialized agents.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.agent.types import A2AClientConfig

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION

if __name__ == "__main__":
    agent = GoogleADKAgent(
        name="GoogleAssistantAgent",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model="gemini-2.0-flash",
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = agent.discover_agents(client_a2a_config)

    response = agent.send_to_agent(agent_cards[0], message="What is the weather in Jakarta?")
    print(response["content"])
