"""Math Tools MCP by STDIO."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math_Tools")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        int: The sum of the two numbers.
    """
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        int: The difference of the two numbers.
    """
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        int: The product of the two numbers.
    """
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> int:
    """Divide two numbers.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        int: The quotient of the two numbers.
    """
    return a / b

@mcp.tool()
def square_root(a: int) -> int:
    """Square root a number.
    Args:
        a: The number to square root.
    Returns:
        int: The square root of the number.
    """
    return a ** 0.5

@mcp.tool()
def power(a: int, b: int) -> int:
    """Raise a number to a power.
    Args:
        a: The number to raise.
        b: The power to raise the number to.
    Returns:
        int: The number raised to the power.
    """
    return a ** b

if __name__ == "__main__":
    mcp.run(transport="sse")
