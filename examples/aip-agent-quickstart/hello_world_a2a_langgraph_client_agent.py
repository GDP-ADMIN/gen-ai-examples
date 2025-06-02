"""Example of a General Assistant LangGraphAgent that can delegate tasks to specialized agents.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.agent.types import A2AClientConfig
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    assistant_agent = LangGraphAgent(
        name="AssistantAgent",
        instruction="You are a helpful assistant that can help with various tasks by delegating to specialized agents.",
        model=ChatOpenAI(model="gpt-4.1"),
        tools=[],
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = assistant_agent.discover_agents(client_a2a_config)
    assistant_agent.register_a2a_agents(agent_cards)

    query = "What is the weather in Jakarta?"
    response = assistant_agent.run(query)
    print(response["output"])
