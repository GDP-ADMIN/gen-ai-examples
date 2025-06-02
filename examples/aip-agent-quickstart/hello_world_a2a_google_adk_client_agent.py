"""Example of a General Assistant GoogleADKAgent that can delegate tasks to specialized agents.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.agent.types import A2AClientConfig

if __name__ == "__main__":
    assistant_agent = GoogleADKAgent(
        name="GoogleAssistantAgent",
        instruction="You are a helpful assistant that can help with various tasks by delegating to specialized agents.",
        model="gemini-2.0-flash",
        tools=[],
        max_iterations=5,
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = assistant_agent.discover_agents(client_a2a_config)
    assistant_agent.register_a2a_agents(agent_cards)

    query = "What is the weather in Jakarta?"
    response = assistant_agent.run(query)
    print(response["output"])
