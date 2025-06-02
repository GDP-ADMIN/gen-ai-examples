"""Hello World arXiv Research Agent Example using LangGraph with MCP SSE transport.

This example demonstrates how to create an arXiv research paper agent using LangGraph
with MCP (Model Context Protocol) over SSE (Server-Sent Events) transport.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

import asyncio
from datetime import datetime

from langchain_openai import ChatOpenAI
from gllm_agents.agent.langgraph_agent import LangGraphAgent
from aip_agent_quickstart.mcp_configs.configs import mcp_config_arxiv_sse


async def main():
    arxiv_agent = LangGraphAgent(
        name="arxiv_research_agent",
        instruction="""You are an expert arXiv research assistant. You help users find and analyze 
        academic papers from arXiv. When searching for papers, you can:
        1. Search by keywords, authors, or topics
        2. Filter by date ranges
        3. Summarize paper abstracts
        4. Provide insights about research trends
        
        Always provide clear, well-structured responses with paper titles, authors, 
        abstracts, and arXiv IDs when available.""",
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[],
    )
    arxiv_agent.add_mcp_server(mcp_config_arxiv_sse)

    query = "Search for research papers about transformer large language models (LLMs) published between January 2025 and May 2025. Focus on papers that discuss Transformer architectures and improvements"
    
    print(f"\nQuery: {query}")
    response = await arxiv_agent.arun(query=query)
    print(f"Response: {response['output']}")


if __name__ == "__main__":
    asyncio.run(main()) 