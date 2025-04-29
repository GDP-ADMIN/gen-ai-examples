from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hello_SSE")

@mcp.tool()
def goodbye_tool(name: str) -> str:
    """This tool says goodbye to the user.

    Args:
        name: The name of the user to say goodbye to.
    Returns:
        A string saying goodbye to the user.
    """
    return f"Goodbye, {name}!"

if __name__ == "__main__":
    mcp.run(transport="sse")