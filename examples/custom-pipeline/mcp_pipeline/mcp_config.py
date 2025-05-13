from typing import Any


def get_mcp_servers(zapier_server_url: str) -> dict[str, Any]:
    mcp_servers = {
        "zapier_github": {
            "url": zapier_server_url,
            "transport": "sse",
        },
    }

    return mcp_servers
