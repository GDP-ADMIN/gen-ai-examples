"""Helper functions for agent operations."""

import sys
import time
from typing import Any, Optional, Tuple, Union

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


def format_tool_call(tool_name: str, input_data: Any) -> str:
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
    from datetime import datetime

    try:
        if isinstance(input_data, (dict, list)):
            formatted_input = json.dumps(input_data, indent=2, ensure_ascii=False)
        else:
            formatted_input = str(input_data)
    except (TypeError, ValueError):
        formatted_input = str(input_data)

    # Truncate long inputs for better readability
    max_length = 500
    if len(formatted_input) > max_length:
        formatted_input = formatted_input[:max_length] + "... [truncated]"

    # Get current timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Create the formatted output
    width = 80
    border = f"{BLUE}╭{'─' * (width-2)}╮{END}"
    tool_header = f"{BOLD}🛠️  [{BLUE}{timestamp}{END}] {YELLOW}{tool_name.upper()}{END}"

    # Format the input lines
    input_lines = [f"{BLUE}│ {CYAN}{line}{END}" for line in formatted_input.split("\n")]

    # Build the formatted output
    formatted = [
        f"\n{border}",
        f"{BLUE}│ {tool_header.ljust(width-3)}{BLUE}│{END}",
        f"{BLUE}├{'─' * (width-2)}┤{END}",
        *input_lines,
        f"{BLUE}╰{'─' * (width-2)}╯{END}",
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
    # ANSI color codes
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"

    from datetime import datetime

    # Extract content from different output formats
    if hasattr(output, "content") and isinstance(getattr(output, "content"), str):
        # If output is an object with a string 'content' attribute (e.g., ToolMessage)
        output_str = getattr(output, "content")
    elif isinstance(output, str):
        output_str = output
    elif isinstance(output, dict):
        # Handle MCP tool output format
        if "tool_output" in output:
            output_str = output["tool_output"]
        else:
            # Try to extract content from common keys
            output_str = output.get("content") or output.get("result") or str(output)
    else:
        output_str = str(output)

    # Truncate long outputs
    max_length = 5000
    if len(output_str) > max_length:
        output_str = output_str[:max_length] + "\n... [truncated]"

    # Get current timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Create the formatted output
    width = 80
    border = f"{GREEN}╭{'─' * (width-2)}╮{END}"
    result_header = f"{BOLD}✅  [{BLUE}{timestamp}{END}] RESULT FROM: {YELLOW}{tool_name.upper()}{END}"

    # Format the output lines
    output_lines = [f"{GREEN}│ {CYAN}{line}{END}" for line in output_str.split("\n")]

    # Build the formatted output
    formatted = [
        f"\n{border}",
        f"{GREEN}│ {result_header.ljust(width-3)}{GREEN}│{END}",
        f"{GREEN}├{'─' * (width-2)}┤{END}",
        *output_lines,
        f"{GREEN}╰{'─' * (width-2)}╯{END}",
    ]

    return "\n".join(formatted)


def extract_final_response(output: Any) -> Optional[str]:
    """Extract the final response from various output formats.

    Args:
        output: The output from the agent

    Returns:
        The extracted response as a string, or None if not found
    """
    if output is None:
        return None

    if hasattr(output, "content"):
        return output.content

    if isinstance(output, dict):
        if "output" in output:
            return output["output"]
        if "content" in output:
            return output["content"]
        if "text" in output:
            return output["text"]
        if (
            "messages" in output
            and isinstance(output["messages"], list)
            and output["messages"]
        ):
            last_msg = output["messages"][-1]
            if hasattr(last_msg, "content"):
                return last_msg.content
            if isinstance(last_msg, dict) and "content" in last_msg:
                return last_msg["content"]
            if hasattr(last_msg, "text"):
                return last_msg.text

    if isinstance(output, list) and output:
        last_item = output[-1]
        if hasattr(last_item, "content"):
            return last_item.content
        if isinstance(last_item, dict):
            return last_item.get("content") or last_item.get("text")

    return str(output)


async def process_events(
    agent, query: str, use_mcp: bool = False
) -> Tuple[Optional[str], int, float]:
    """Process agent events and return the final response and metrics.

    Args:
        agent: The research agent
        query: The user's query
        use_mcp: Whether to use MCP mode (True) or A2A mode (False)

    Returns:
        Tuple containing (final_response, tool_call_count, processing_time)
    """
    start_time = time.time()
    tool_call_count = 0
    response_chunks = []
    final_response = None

    try:
        if use_mcp:
            # MCP mode - use arun_stream
            tool_calls = set()  # Track unique tool calls

            async for chunk in agent.arun_stream(query=query):
                if isinstance(chunk, dict):
                    # Handle tool calls - MCP uses 'tool' and 'input' keys
                    if "tool" in chunk and chunk["tool"]:
                        tool_name = chunk.get("tool", "unknown")
                        tool_input = chunk.get("input", {}) or chunk.get(
                            "tool_input", {}
                        )

                        # Only count unique tool calls
                        tool_call_id = f"{tool_name}-{str(tool_input)}"
                        if tool_call_id not in tool_calls:
                            tool_calls.add(tool_call_id)
                            tool_call_count += 1
                            print(format_tool_call(tool_name, tool_input))

                    # Handle tool results
                    if "tool_output" in chunk and chunk["tool_output"]:
                        print(
                            format_tool_result(
                                "MCP Tool Result", chunk.get("tool_output", {})
                            )
                        )

                    # Handle content
                    if "content" in chunk and chunk["content"]:
                        content = chunk["content"]
                        if isinstance(content, str) and content.strip():
                            response_chunks.append(content)
                elif isinstance(chunk, str) and chunk.strip():
                    response_chunks.append(chunk)

            if response_chunks:
                final_response = "".join(response_chunks)
        else:
            # A2A mode - use agent_executor.astream_events
            async for event in agent.agent_executor.astream_events(
                {"messages": [HumanMessage(content=query)]}, version="v2"
            ):
                event_type = event["event"]
                data = event.get("data", {})

                if event_type == "on_tool_start":
                    tool_call_count += 1
                    print(
                        format_tool_call(
                            event.get("name", "unknown"), data.get("input", {})
                        )
                    )

                elif event_type == "on_tool_end":
                    print(
                        format_tool_result(
                            event.get("name", "unknown"), data.get("output", "")
                        )
                    )

                elif event_type == "on_chain_end":
                    final_output = data.get("output", {})
                    final_response = extract_final_response(final_output)

                # Handle any additional events if needed
                # ...

        # If we have response chunks but no final response, join them
        if not final_response and response_chunks:
            final_response = "".join(response_chunks)

    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(f"Error in process_events: {e}", file=sys.stderr)
        return error_msg, tool_call_count, time.time() - start_time

    processing_time = time.time() - start_time
    return final_response, tool_call_count, processing_time


async def process_query(agent, query: str, use_mcp: bool = False) -> str:
    """Process a user query with the research agent.

    Args:
        agent: The research agent
        query: The user's query
        use_mcp: Whether to use MCP mode (True) or A2A mode (False)

    Returns:
        str: The agent's response
    """
    print(f"\n{'=' * 120}")
    print(f"QUERY: {query}")
    print(f"{'=' * 120}")

    final_response, tool_call_count, processing_time = await process_events(
        agent, query, use_mcp=use_mcp
    )

    # Print performance metrics
    print("\n" + "=" * 120)
    print("PERFORMANCE METRICS".center(120))
    print("=" * 120)
    print(f"Tool calls: {tool_call_count}")
    print(f"Processing time: {processing_time:.2f} seconds")
    print("=" * 120 + "\n")

    return final_response if final_response else "No response was generated."
