"""Example of a General Assistant LangChainAgent that can delegate tasks to specialized agents.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.agent.types import A2AClientConfig
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    assistant_agent = LangChainAgent(
        name="AssistantAgentLangChain",
        instruction="You are a helpful assistant that can help with various tasks by delegating to specialized agents.",
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = assistant_agent.discover_agents(client_a2a_config)
    assistant_agent.register_a2a_agents(agent_cards)

    query = "What is the weather in Jakarta?"
    response = assistant_agent.run(query)
    print(response["output"])
