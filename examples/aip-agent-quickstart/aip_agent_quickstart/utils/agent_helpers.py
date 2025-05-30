"""Helper functions for agent operations."""

import time
from typing import Any, Dict, Optional, Tuple, Union

from langchain_core.messages import HumanMessage


def print_response(response: Union[str, Any]) -> None:
    """Print the response in a visually appealing format with colors and formatting.

    Args:
        response: The response to print, can be string or any other type
    """
    if not isinstance(response, str):
        response = str(response)

    # ANSI color codes
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    END = "\033[0m"

    # Format the response
    lines = response.strip().split("\n")
    formatted_lines = []

    for line in lines:
        # Format section headers (lines that end with a colon)
        if line.strip().endswith(":"):
            formatted_lines.append(f"\n{YELLOW}{BOLD}{line.upper()}{END}")
        # Format list items
        elif line.strip().startswith(("- ", "* ", "• ")):
            formatted_lines.append(f"{GREEN}•{END} {line[2:].strip()}")
        # Format code blocks
        elif line.strip().startswith("```"):
            formatted_lines.append(f"{BLUE}{line}{END}")
        # Format URLs
        elif "http" in line:
            formatted_lines.append(f"{CYAN}{line}{END}")
        else:
            formatted_lines.append(line)

    # Join the formatted lines
    formatted_response = "\n".join(formatted_lines)

    # Print the response with a nice border
    width = min(120, 120)  # Max width for readability
    border = f"{BLUE}{'=' * width}{END}"

    print(f"\n{border}")
    print(f"{GREEN}{BOLD}{' 🤖 AGENT RESPONSE '.center(width, ' ')}{END}")
    print(f"{border}")
    print(formatted_response)
    print(f"{border}\n")


def format_section(title: str, char: str = "=", width: int = 120) -> None:
    """Print a formatted section header with colors and styling.

    Args:
        title: The title to display
        char: Character to use for the separator line (ignored, kept for backward compatibility)
        width: Width of the separator line
    """
    # ANSI color codes
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    END = "\033[0m"

    # Define section styles based on title
    if "error" in title.lower():
        color = "\033[91m"  # Red for errors
        icon = "❌"
    elif "warning" in title.lower():
        color = YELLOW
        icon = "⚠️ "
    elif "success" in title.lower():
        color = GREEN
        icon = "✅ "
    else:
        color = CYAN
        icon = "📌 "

    # Create the formatted section
    border = f"{BLUE}{'━' * width}{END}"
    title_text = f"{BOLD}{color}{icon}{title.upper()}{END}"

    print(f"\n{border}")
    print(title_text)
    print(border)


def format_tool_call(tool_name: str, input_data: Dict[str, Any]) -> str:
    """Format tool call information with colors and styling.

    Args:
        tool_name: Name of the tool being called
        input_data: Input parameters for the tool

    Returns:
        Formatted tool call string with colors and styling
    """
    # ANSI color codes
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    END = "\033[0m"

    # Format the input data as pretty-printed JSON
    import json

    formatted_input = json.dumps(input_data, indent=2) if input_data else "No input"

    # Create the formatted output
    width = 120
    border = f"{BLUE}{'━' * width}{END}"
    tool_header = f"{BOLD}🛠️  TOOL CALL: {YELLOW}{tool_name}{END}"

    formatted = [
        f"\n{border}",
        tool_header,
        f"{BLUE}┃{END}",
        f"{CYAN}{formatted_input}{END}",
        border,
    ]

    return "\n".join(formatted)


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


async def process_events(agent, query: str) -> Tuple[Optional[str], int, float]:
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
                    final_response = str(final_output)

        processing_time = time.time() - start_time
        return final_response, tool_call_count, processing_time

    except Exception as e:
        processing_time = time.time() - start_time
        return str(e), tool_call_count, processing_time


async def process_query(agent, query: str) -> str:
    """Process a user query with the research agent.

    Args:
        agent: The research agent
        query: The user's query

    Returns:
        str: The agent's response
    """
    print(f"\n{'=' * 120}")
    print(f"QUERY: {query}")
    print(f"{'=' * 120}")

    final_response, tool_call_count, processing_time = await process_events(
        agent, query
    )

    # Print performance metrics
    print("\n" + "=" * 120)
    print("PERFORMANCE METRICS".center(120))
    print("=" * 120)
    print(f"Tool calls: {tool_call_count}")
    print(f"Processing time: {processing_time:.2f} seconds")
    print("=" * 120 + "\n")

    return final_response if final_response else "No response was generated."
