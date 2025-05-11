from typing import Any


def get_mcp_servers() -> dict[str, Any]:
    mcp_servers = {
        "math_tools": {
            # "command": "python",
            # "args": ["mcp_pipeline/mcp_math.py"],
            # "transport": "stdio",
            "url": "http://localhost:8000/sse",
            "transport": "sse",
        },
    }

    return mcp_servers
