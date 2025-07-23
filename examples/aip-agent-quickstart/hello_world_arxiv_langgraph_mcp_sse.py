"""Hello World arXiv Research Agent Example using LangGraph with MCP SSE transport.

This example demonstrates how to create an arXiv research paper agent using LangGraph
with MCP (Model Context Protocol) over SSE (Server-Sent Events) transport.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config.agent import ARXIV_AGENT_INSTRUCTION
from aip_agent_quickstart.mcp_configs.configs import mcp_config_arxiv_sse

if __name__ == "__main__":
    arxiv_agent = LangGraphAgent(
        name="arxiv_research_agent",
        instruction=ARXIV_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
    )
    arxiv_agent.add_mcp_server(mcp_config_arxiv_sse)

    response = arxiv_agent.run(
        query="""Search for research papers about transformer large language models (LLMs) published between
        January 2024 and May 2024. Focus on papers that discuss Transformer architectures and improvements."""
    )
    print(f"Response: {response['output']}")
