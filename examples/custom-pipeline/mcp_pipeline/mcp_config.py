from typing import Any


def get_mcp_servers(server_url: str) -> dict[str, Any]:
    mcp_servers = {
        "gdp": {
            "url": server_url,
            "transport": "sse",
        },
    }

    return mcp_servers
