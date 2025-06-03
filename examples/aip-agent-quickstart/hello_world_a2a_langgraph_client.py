"""Example of a General Assistant LangGraphAgent that can delegate tasks to specialized agents.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.agent.types import A2AClientConfig
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION

if __name__ == "__main__":
    agent = LangGraphAgent(
        name="AssistantAgent",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1"),
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = agent.discover_agents(client_a2a_config)

    response = agent.send_to_agent(agent_cards[0], message="What is the weather in Jakarta?")
    print(response["content"])
