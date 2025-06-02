"""Example of a General Assistant LangChainAgent that can delegate tasks to specialized agents.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

from gllm_agents.agent.langchain_agent import LangChainAgent
from gllm_agents.agent.types import A2AClientConfig
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION

if __name__ == "__main__":
    agent = LangChainAgent(
        name="AssistantAgentLangChain",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
    )

    client_a2a_config = A2AClientConfig(discovery_urls=["http://localhost:8001"])
    agent_cards = agent.discover_agents(client_a2a_config)
    agent.register_a2a_agents(agent_cards)

    response = agent.run(query="What is the weather in Jakarta?")
    print(response["output"])
