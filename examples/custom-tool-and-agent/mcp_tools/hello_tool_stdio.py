from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hello_STDIO")

@mcp.tool()
def hello_tool(name: str) -> str:
    """This tool says hello to the user.

    Args:
        name: The name of the user to say hello to.
    Returns:
        A string saying hello to the user.
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="stdio")
