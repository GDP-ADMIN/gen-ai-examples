"""Minimal LangGraph agent with bosa support example demonstrating asynchronous run.

Authors:
    Saul Sayers (saul.sayers@gdplabs.id)
"""

import asyncio
from langchain_openai import ChatOpenAI

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from aip_agent_quickstart.tools.twitter_bosa_tool import twitter_get_user_tool


async def main():
    """Demonstrates the LangGraphAgent's arun method."""
    model = ChatOpenAI(model="gpt-4.1", temperature=0)
    tools = [twitter_get_user_tool]
    agent_name = "BOSAConnectorTwitterAgent"

    langgraph_agent = LangGraphAgent(
        name=agent_name,
        instruction="You are a helpful assistant that use BOSA connector to connect with Twitter API.",
        model=model,
        tools=tools,
    )

    query = "Get me user details for Twitter user @elonmusk"
    print(f"--- Agent: {agent_name} ---")
    print(f"Query: {query}")

    print("\nRunning arun...")
    response = await langgraph_agent.arun(
        query=query,
        configurable={"configurable": {"thread_id": "lgraph_arith_example_arun"}},
    )
    print(f"[arun] Final Response: {response}")
    print("--- End of LangGraph Example ---")


if __name__ == "__main__":
    # OPENAI_API_KEY should be set in the environment.
    asyncio.run(main())
