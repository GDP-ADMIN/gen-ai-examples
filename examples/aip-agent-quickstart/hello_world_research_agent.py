"""Hello World Research Agent Example.

This example demonstrates how to create and use the Research Agent that can:
1. Handle academic queries using the arXiv MCP tools
2. Handle travel planning queries by delegating to specialized A2A agents
3. Recognize and respond appropriately to unsupported query topics

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

import asyncio
import time
from typing import Any, Dict, List, Optional, Tuple

from langchain_core.messages import HumanMessage

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
    if not discovery_urls:
        # Default discovery URLs including the web search agent
        discovery_urls = ["http://localhost:8002"]  # Web search agent runs on port 8002

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


def format_section(title: str, char: str = "=", width: int = 120) -> None:
    """Print a formatted section header.

    Args:
        title: The title to display
        char: Character to use for the separator line
        width: Width of the separator line
    """
    print(f"\n{char * width}")
    print(title.upper())
    print(f"{char * width}")


def format_tool_call(tool_name: str, input_data: Dict[str, Any]) -> str:
    """Format tool call information.

    Args:
        tool_name: Name of the tool being called
        input_data: Input parameters for the tool

    Returns:
        Formatted tool call string
    """
    sep = "-" * 120
    return sep + f"\n[TOOL] {tool_name}\n" + sep + f"\nInput: {input_data}"


def format_tool_result(tool_name: str, output: Any) -> str:
    """Format tool result with truncation if needed, prioritizing 'content' attribute.

    Args:
        tool_name: Name of the tool that produced the result
        output: The output from the tool

    Returns:
        Formatted tool result string
    """
    if hasattr(output, "content") and isinstance(getattr(output, "content"), str):
        # If output is an object with a string 'content' attribute (e.g., ToolMessage)
        output_str = getattr(output, "content")
    elif isinstance(output, str):
        output_str = output
    else:
        # Fallback for other types or if content is not a simple string
        output_str = str(output)

    # Using the emoji and style observed in logs for tool output display
    return f"\n📥 Output:\n{output_str}\n"


async def process_events(
    agent: LangGraphAgent, query: str
) -> Tuple[Optional[str], int, float]:
    """Process agent events and return the final response and metrics.

    Args:
        agent: The research agent
        query: The user's query

    Returns:
        Tuple containing (final_response, tool_call_count, processing_time)
    """
    start_time = time.time()
    tool_call_count = 0
    final_response = None

    try:
        async for event in agent.agent_executor.astream_events(
            {"messages": [HumanMessage(content=query)]}, version="v2"
        ):
            event_type = event["event"]
            data = event.get("data", {})

            if event_type == "on_tool_start":
                tool_call_count += 1
                print(format_tool_call(event["name"], data.get("input", {})))

            elif event_type == "on_tool_end":
                print(format_tool_result(event["name"], data.get("output", "")))

            elif event_type == "on_chain_end":
                final_output = data.get("output", {})
                final_response = None

                try:
                    # First, handle the case where final_output is a message object
                    if hasattr(final_output, "content"):
                        final_response = final_output.content
                    # Handle dictionary outputs
                    elif isinstance(final_output, dict):
                        # Try to get the response from common keys
                        if "output" in final_output:
                            final_response = final_output["output"]
                        elif "content" in final_output:
                            final_response = final_output["content"]
                        elif "text" in final_output:
                            final_response = final_output["text"]
                        # Handle messages array if present
                        elif (
                            "messages" in final_output
                            and isinstance(final_output["messages"], list)
                            and final_output["messages"]
                        ):
                            last_msg = final_output["messages"][-1]
                            if hasattr(last_msg, "content"):
                                final_response = last_msg.content
                            elif isinstance(last_msg, dict) and "content" in last_msg:
                                final_response = last_msg["content"]
                            elif hasattr(last_msg, "text"):
                                final_response = last_msg.text
                    # Handle list outputs
                    elif isinstance(final_output, list) and final_output:
                        last_item = final_output[-1]
                        if hasattr(last_item, "content"):
                            final_response = last_item.content
                        elif isinstance(last_item, dict):
                            final_response = (
                                last_item.get("content")
                                or last_item.get("text")
                                or str(last_item)
                            )
                        else:
                            final_response = str(last_item)
                except Exception as e:
                    print(f"[DEBUG] Error processing output: {e}")

                # Final fallback
                if final_response is None:
                    final_response = (
                        str(final_output)
                        if final_output is not None
                        else "No response generated"
                    )

    except Exception as e:
        print(f"\n[ERROR] Error processing events: {e}")
        import traceback

        traceback.print_exc()

    processing_time = time.time() - start_time
    return final_response, tool_call_count, processing_time


async def process_query(agent: LangGraphAgent, query: str) -> str:
    """Process a user query with the research agent.

    Args:
        agent: The research agent
        query: The user's query

    Returns:
        str: The agent's response
    """
    format_section(f"Processing query: {query}")
    try:
        # Process events and get metrics
        final_response, tool_call_count, processing_time = await process_events(
            agent, query
        )

        # Print the final response with better formatting
        format_section("Final Response", "-")
        print(final_response)

        # Print performance metrics
        print("\n" + "=" * 120)
        print("PERFORMANCE METRICS".center(120))
        print("=" * 120)
        print(f"Tool calls: {tool_call_count}")
        print(f"Processing time: {processing_time:.2f} seconds")
        print("=" * 120 + "\n")

        return final_response if final_response else "No response was generated."

    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(f"\n[ERROR] {error_msg}")
        import traceback

        traceback.print_exc()
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


async def demo_with_mcp(agent):
    """Step 2: Add MCP server for academic research capabilities."""
    print("\n--- STEP 2: RESEARCH AGENT WITH ARXIV MCP SERVER ---")

    agent.add_mcp_server(mcp_config_arxiv_sse)
    logger.info("Added arXiv MCP server to the Research Agent")

    # Test with an academic query that should use arXiv tools
    await process_query(
        agent,
        "Find recent papers about transformer models in natural language processing published in 2025",
    )


async def demo_with_a2a(agent):
    """Step 3: Register and test A2A agents including the web search agent."""
    print("\n--- STEP 3: RESEARCH AGENT WITH A2A AGENTS ---")

    # Register A2A agents with explicit web search agent URL
    # web_search_url = "http://localhost:8002"
    web_search_url = "https://mcp.obrol.id/b"
    information_compiler_url = "http://localhost:8003"
    # information_compiler_url = "https://mcp.obrol.id/c" # WIP

    print("Registering A2A agents...")
    await register_a2a_agents(
        agent, discovery_urls=[web_search_url, information_compiler_url]
    )
    print("Agents registered successfully!\n")

    # Test with a travel planning query that should use A2A agents
    travel_query = (
        "Plan a 5-day trip to Bali for two people with a $2500 budget, including flights from Singapore."
        "Include estimated costs for each category and daily breakdown."
    )
    await process_query(agent, travel_query)


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


async def main():
    """Run the Research Agent examples progressively."""
    print("=== RESEARCH AGENT DEMO ===")

    # Step 1: Define a single agent - run demo but don't save the agent
    agent = await demo_single_agent()

    # Step 2: Add MCP server - run demo but don't save the agent
    # await demo_with_mcp(agent)

    # Step 3: Add A2A agents (we don't need to store the agent since we're not using it further)
    await demo_with_a2a(agent)

    # Step 4: Start interactive query session
    # await interactive_query_session(agent)

    print("\n=== DEMO COMPLETED ===")


if __name__ == "__main__":
    # OPENAI_API_KEY should be set in the environment
    asyncio.run(main())
