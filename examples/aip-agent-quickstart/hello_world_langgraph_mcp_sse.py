"""Example showing LangGraph agent with MCP tools integration.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION
from aip_agent_quickstart.mcp_configs.configs import mcp_config_sse

if __name__ == "__main__":
    langgraph_agent = LangGraphAgent(
        name="langgraph_mcp_example",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
    )
    langgraph_agent.add_mcp_server(mcp_config_sse)

    response = langgraph_agent.run(query="What's the weather forecast for monday?")
    print(f"Response: {response.get('output')}")
