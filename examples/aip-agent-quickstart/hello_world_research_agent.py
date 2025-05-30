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

from langchain_openai import ChatOpenAI

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.agent.types import A2AClientConfig
from gllm_agents.utils.logger_manager import LoggerManager

from aip_agent_quickstart.agents.research_agent.research_agent.config import (
    RESEARCH_AGENT_INSTRUCTION,
)
from aip_agent_quickstart.mcp_configs.configs import mcp_config_arxiv_sse
from aip_agent_quickstart.utils import format_section, process_query, print_response

# Configure logging
logger = LoggerManager().get_logger(__name__)


async def create_research_agent() -> LangGraphAgent:
    """Create and configure the Research Agent.

    Returns:
        LangGraphAgent: The configured research agent
    """
    return LangGraphAgent(
        name="ResearchAgent",
        instruction=RESEARCH_AGENT_INSTRUCTION,
        model=ChatOpenAI(model="gpt-4.1", temperature=0),
        # verbose=True,
    )


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

        logger.error(f"Failed to register A2A agents: {e}")
        return agent


async def demo_single_agent():
    """Create and test a basic research agent with no external services."""
    agent = await create_research_agent()

    # Test with a query that doesn't require external services
    response = await process_query(
        agent,
        "What kinds of topics can you help me with?",
    )

    print_response(response)
    return agent


async def demo_with_mcp(agent):
    """Add MCP server for academic research capabilities."""
    print("Adding arXiv MCP server to the Research Agent...")
    agent.add_mcp_server(mcp_config_arxiv_sse)
    logger.info("Added arXiv MCP server to the Research Agent")

    # Enable debug logging for MCP server
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.getLogger("aip_agent_quickstart.mcp_configs").setLevel(logging.DEBUG)

    # Test with an academic query that should use arXiv tools
    response = await process_query(
        agent,
        "Find recent papers about transformer models in natural language processing published in 2023-2024",
    )

    print_response(response)
    return agent


async def demo_with_a2a(agent):
    """Register and test A2A agents including the web search agent."""
    print("Registering A2A agents...")

    # Register A2A agents with explicit web search agent URL
    web_search_url = "https://mcp.obrol.id/b"
    information_compiler_url = "https://mcp.obrol.id/c"

    await register_a2a_agents(
        agent, discovery_urls=[web_search_url, information_compiler_url]
    )
    print("Agents registered successfully!")

    # Test with a query that should use A2A agents
    response = await process_query(
        agent,
        "What are the latest developments in AI as of 2024?",
    )
    print_response(response)

    # Test with a travel planning query
    travel_query = (
        "Plan a 5-day trip to Bali for two people with a $2500 budget, including flights from Singapore. "
        "Include estimated costs for each category and daily breakdown."
    )
    response = await process_query(agent, travel_query)
    print_response(response)
    return agent


async def interactive_query_session(agent):
    """Start an interactive session to ask questions to the Research Agent."""
    print("\n=== Interactive Query Session ===")
    while True:
        try:
            query = input("\nYour question: ").strip()
            print("\nProcessing your question...")
            response = await process_query(agent, query)
            print(f"\nResponse: {response}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            continue
        finally:
            print("\nThank you for using the Research Agent. Goodbye!")


def display_menu(agent_initialized: bool = False) -> int:
    """Display the mode selection menu and get user choice.

    Args:
        agent_initialized: Whether an agent has been initialized
    """
    format_section("Research Agent Demo")
    print("Select mode to run:")
    print("1. Single Agent (Basic mode with no external services)")
    print("2. Agent with MCP (Academic research capabilities)")
    print("3. Agent with A2A (Web search and information compilation)")
    if agent_initialized:
        print("4. Interactive Query Session (Use current agent configuration)")
    print("0. Exit")

    max_choice = 4 if agent_initialized else 3

    while True:
        try:
            choice = int(input(f"\nEnter your choice (0-{max_choice}): "))
            if 0 <= choice <= max_choice and (choice != 4 or agent_initialized):
                return choice
            print(f"Please enter a number between 0 and {max_choice}")
        except ValueError:
            print("Please enter a valid number")


async def main():
    """Run the Research Agent with user-selected mode."""
    current_agent = None

    while True:
        choice = display_menu(agent_initialized=current_agent is not None)

        if choice == 0:
            print("Exiting...")
            break

        try:
            if choice == 1:  # Single Agent
                format_section("Single Agent Mode")
                current_agent = await demo_single_agent()

            elif choice == 2:  # MCP
                format_section("Agent with MCP")
                current_agent = await create_research_agent()
                await demo_with_mcp(current_agent)

            elif choice == 3:  # A2A
                format_section("Agent with A2A")
                current_agent = await create_research_agent()
                await demo_with_a2a(current_agent)

            elif choice == 4 and current_agent:  # Interactive Query Session
                format_section("Interactive Query Session")
                await interactive_query_session(current_agent)
                input("\nPress Enter to return to the main menu...")

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            import traceback

            traceback.print_exc()
            input("\nPress Enter to continue...")

    print("\n=== DEMO COMPLETED ===")


if __name__ == "__main__":
    # OPENAI_API_KEY should be set in the environment
    asyncio.run(main())
