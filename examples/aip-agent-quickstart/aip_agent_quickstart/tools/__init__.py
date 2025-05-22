"""Tools for the AIP Agent Quickstart package."""

from langchain.tools import tool
from typing import Union

@tool
def add_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b
