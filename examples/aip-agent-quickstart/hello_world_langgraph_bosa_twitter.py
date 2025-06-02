"""Minimal LangGraph agent with bosa support example demonstrating asynchronous run.

Authors:
    Saul Sayers (saul.sayers@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.tools.twitter_bosa_tool import twitter_get_user_tool

if __name__ == "__main__":
    langgraph_agent = LangGraphAgent(
        name="BOSAConnectorTwitterAgent",
        instruction="You are a helpful assistant that use BOSA connector to connect with Twitter API.",
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        tools=[twitter_get_user_tool],
    )

    response = langgraph_agent.run(query="Get me user details for Twitter user @elonmusk")
    print(response["output"])
