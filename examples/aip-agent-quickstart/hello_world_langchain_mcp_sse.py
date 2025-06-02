"""Example showing LangChain agent with MCP tools integration using SSE transport.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

from gllm_agents.agent.langchain_agent import LangChainAgent
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.mcp_configs.configs import mcp_config_sse

if __name__ == "__main__":
    langchain_agent = LangChainAgent(
        name="langchain_mcp_example",
        instruction="You are a helpful assistant that can provide weather forecasts.",
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
        agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    )
    langchain_agent.add_mcp_server(mcp_config_sse)

    response = langchain_agent.run(query="What's the weather forecast for monday?")
    print(f"Response: {response.get('output')}")
