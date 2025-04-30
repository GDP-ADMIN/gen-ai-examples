"""Text Frequency Counter MCP by SSE."""

import json
import re
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Dict

mcp = FastMCP("Text_Frequency_Counter")

@mcp.tool()
def text_frequency_counter(
    text: str = Field(default="", description="The text to count the frequency of each word in.")
) -> Dict[str, int]:
    """This tool counts the frequency of each word in the text.

    Args:
        text: The text to count the frequency of each word in.
    Returns:
        Dict[str, int]: The dictionary of words and their frequencies. This output can be used as input to the sort_frequencies tool.
    """
    text = text.lower()
    words = text.split()
    words = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in words]
    return {word: words.count(word) for word in words}

@mcp.tool()
def sort_frequencies(
    frequencies: Dict[str, int] = Field(
        default_factory=dict,
        description="The dictionary of words and their frequencies to sort. This should be the output from text_frequency_counter."
    )
) -> Dict[str, int]:
    """This tool sorts the frequencies of the words in the text.

    Args:
        frequencies: The dictionary of words and their frequencies. This should be the output from text_frequency_counter.
    Returns:
        Dict[str, int]: The dictionary of words sorted by frequency.
    """
    sorted_items = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_items)

@mcp.tool()
def to_json(
    data: Dict[str, int] = Field(
        default_factory=dict,
        description="The dictionary of words and their frequencies to convert to JSON."
    )
) -> str:
    """This tool converts a dictionary of words and their frequencies to a JSON string.

    Args:
        data: The dictionary of words and their frequencies to convert to JSON.
    Returns:
        str: The JSON string of the dictionary of words and their frequencies.
    """
    return json.dumps(data)

if __name__ == "__main__":
    mcp.run(transport="sse")
