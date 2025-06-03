"""Example showing LangChain agent with MCP tools integration using stdio transport.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

from gllm_agents.agent.langchain_agent import LangChainAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION
from aip_agent_quickstart.mcp_configs.configs import mcp_config_stdio

if __name__ == "__main__":
    langchain_agent = LangChainAgent(
        name="langchain_mcp_example",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        llm=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
    )
    langchain_agent.add_mcp_server(mcp_config_stdio)

    response = langchain_agent.run(query="What's the weather forecast for monday?")
    print(f"Response: {response.get('output')}")
