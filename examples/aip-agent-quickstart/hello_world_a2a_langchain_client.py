"""Example of a General Assistant LangChainAgent that can delegate tasks to specialized agents.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.agent.types import A2AClientConfig
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    agent = LangChainAgent(
        name="AssistantAgentLangChain",
        instruction="You are a helpful assistant that can help with various tasks by delegating to specialized agents.",
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = agent.discover_agents(client_a2a_config)

    response = agent.send_to_agent(agent_cards[0], query="What is the weather in Jakarta?")
    print(response.get("content", str(response)))
