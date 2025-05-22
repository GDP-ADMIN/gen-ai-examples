"""LangChain-specific arithmetic tools for GLLM agent examples."""

from langchain_core.tools import tool


# Decorate the plain function to create a LangChain Tool
@tool
def add_numbers(a: int, b: int) -> str:
    """Adds two numbers and returns the result as a string.

    This is a self-contained LangChain tool.
    For example:
    add_numbers(a=5, b=3)
    """
    try:
        result = a + b
        return str(result)
    except Exception as e:
        return f"Error: Could not add numbers. Reason: {str(e)}"


# You could also export it with a more specific name if preferred, e.g.:
# langchain_add_tool = add_numbers
