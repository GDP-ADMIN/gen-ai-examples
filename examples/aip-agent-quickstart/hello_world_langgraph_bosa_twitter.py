"""Minimal LangGraph agent with bosa support example demonstrating asynchronous run.

Authors:
    Saul Sayers (saul.sayers@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION
from aip_agent_quickstart.tools import bosa_twitter_tools

if __name__ == "__main__":

    langgraph_agent = LangGraphAgent(
        name="BOSAConnectorTwitterAgent",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=bosa_twitter_tools,
    )

    response = langgraph_agent.run(query="Get me user details for Twitter user @elonmusk")
    print(response["output"])
