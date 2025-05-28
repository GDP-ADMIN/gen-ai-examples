"""Hello World Research Agent Example.

This example demonstrates how to create and use the Research Agent that can:
1. Handle academic queries using the arXiv MCP tools
2. Handle travel planning queries by delegating to specialized A2A agents
3. Recognize and respond appropriately to unsupported query topics

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

import asyncio
from typing import List, Optional

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.agent.types import A2AClientConfig
from gllm_agents.utils.logger_manager import LoggerManager
from langchain_openai import ChatOpenAI

from aip_agent_quickstart.agents.research_agent.research_agent.config import (
    RESEARCH_AGENT_INSTRUCTION,
)
from aip_agent_quickstart.mcp_configs.configs import mcp_config_arxiv_sse

# Configure logging
logger = LoggerManager().get_logger(__name__)


async def create_research_agent() -> LangGraphAgent:
    """Create and configure the Research Agent.

    Returns:
        LangGraphAgent: The configured research agent
    """
    # Create the LLM
    llm = ChatOpenAI(model="gpt-4.1", temperature=0)

    # Create the Research Agent with the instruction but no tools yet
    research_agent = LangGraphAgent(
        name="ResearchAgent",
        instruction=RESEARCH_AGENT_INSTRUCTION,
        model=llm,
        tools=[],
        verbose=True,
    )

    return research_agent


async def add_mcp_server(agent: LangGraphAgent) -> LangGraphAgent:
    """Add MCP server configuration to the agent for accessing arXiv tools.

    Args:
        agent: The research agent

    Returns:
        LangGraphAgent: The updated research agent with MCP server access
    """
    # Add the arXiv MCP server configuration
    agent.add_mcp_server(mcp_config_arxiv_sse)
    logger.info("Added arXiv MCP server to the Research Agent")

    return agent


async def register_a2a_agents(
    agent: LangGraphAgent, discovery_urls: Optional[List[str]] = None
) -> LangGraphAgent:
    """Discover and register available A2A agents for travel planning.

    Args:
        agent: The research agent
        discovery_urls: Optional list of URLs for A2A agent discovery

    Returns:
        LangGraphAgent: The updated research agent with registered A2A agents
    """
    if not discovery_urls:
        # Default discovery URLs (information_compiler_agent and web_search_agent would be here)
        # Currently these are placeholder URLs as the agents are not yet implemented
        discovery_urls = ["http://localhost:8003", "http://localhost:8004"]

    # Configure A2A client
    client_a2a_config = A2AClientConfig(discovery_urls=discovery_urls)

    try:
        # Attempt to discover agents
        agent_cards = agent.discover_agents(client_a2a_config)

        # Register discovered agents
        agent.register_a2a_agents(agent_cards)
        logger.info(f"Registered {len(agent_cards)} A2A agents")
    except Exception as e:
        logger.warning(f"Failed to discover A2A agents: {e}")
        logger.warning("Continuing without A2A agents...")

    return agent


async def process_query(agent: LangGraphAgent, query: str) -> str:
    """Process a user query with the research agent.

    Args:
        agent: The research agent
        query: The user's query

    Returns:
        str: The agent's response
    """
    print(f"\nProcessing query: {query}")

    try:
        # Run the agent with the query
        response = await agent.arun(query=query)
        result = response.get("output", "")

        print(f"Agent response: {result}")
        return result
    except Exception as e:
        error_msg = f"Error processing query: {e}"
        print(error_msg)
        return error_msg


async def demo_single_agent():
    """Step 1: Create and test a basic research agent with no external services."""
    print("\n--- STEP 1: BASIC RESEARCH AGENT ---")
    agent = await create_research_agent()

    # Test with a query that doesn't require external services
    await process_query(
        agent,
        "What kinds of topics can you help me with?",
    )

    return agent


async def demo_with_mcp():
    """Step 2: Add MCP server for academic research capabilities."""
    print("\n--- STEP 2: RESEARCH AGENT WITH ARXIV MCP SERVER ---")
    agent = await create_research_agent()
    agent = await add_mcp_server(agent)

    # Test with an academic query that should use arXiv tools
    await process_query(
        agent,
        "Find recent papers about transformer models in natural language processing published in 2025",
    )

    return agent


async def demo_with_a2a():
    """Step 3: Register A2A agents for travel planning capabilities."""
    print("\n--- STEP 3: RESEARCH AGENT WITH A2A AGENTS ---")
    agent = await create_research_agent()
    agent = await add_mcp_server(agent)
    agent = await register_a2a_agents(agent)

    # Note: This would use A2A agents if available, but may fall back to general capabilities
    # if the A2A agents are not accessible
    await process_query(
        agent,
        "Plan a 3-day trip to Bali with budget considerations",
    )

    return agent


async def test_query_types(agent: LangGraphAgent):
    """Step 4-6: Test various query types to demonstrate the agent's capabilities."""
    print("\n--- TESTING DIFFERENT QUERY TYPES ---")

    # Step 4: Academic query (should use arXiv MCP tools)
    print("\n--- STEP 4: ACADEMIC QUERY ---")
    await process_query(
        agent,
        "Summarize research trends in transformer models from 2023-2025",
    )

    # Step 5: Travel query (should use A2A agents if available)
    print("\n--- STEP 5: TRAVEL QUERY ---")
    await process_query(
        agent,
        "What are popular tourist spots in Tokyo?",
    )

    # Step 6: Unsupported query (should return a message about limitations)
    print("\n--- STEP 6: UNSUPPORTED QUERY ---")
    await process_query(
        agent,
        "What's the weather forecast for Jakarta today?",
    )


async def main():
    """Run the Research Agent examples progressively."""
    print("=== RESEARCH AGENT DEMO ===")

    # Step 1: Define a single agent - run demo but don't save the agent
    await demo_single_agent()

    # Step 2: Add MCP server - run demo but don't save the agent
    await demo_with_mcp()

    # Step 3: Add A2A agents (we don't need to store the agent since we're not using it further)
    await demo_with_a2a()

    # Steps 4-6: Test different query types (commented out as we're not using it)
    # await test_query_types(agent3)

    print("\n=== DEMO COMPLETED ===")


if __name__ == "__main__":
    # OPENAI_API_KEY should be set in the environment
    asyncio.run(main())
