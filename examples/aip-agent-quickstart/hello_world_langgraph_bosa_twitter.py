"""Minimal LangGraph agent with bosa support example demonstrating asynchronous run.

Authors:
    Saul Sayers (saul.sayers@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

import os
from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION
from bosa_connectors import BOSAConnectorToolGenerator

if __name__ == "__main__":
    bosa_connector_tool_generator = BOSAConnectorToolGenerator(
        api_base_url=os.getenv("BOSA_API_BASE_URL", "https://staging-api.bosa.id"),
        api_key=os.getenv("BOSA_API_KEY", ""),
        app_name="twitter",
    )
    tools = bosa_connector_tool_generator.generate_tools()

    langgraph_agent = LangGraphAgent(
        name="BOSAConnectorTwitterAgent",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=tools,
    )

    response = langgraph_agent.run(query="Get me user details for Twitter user @elonmusk")
    print(response["output"])
