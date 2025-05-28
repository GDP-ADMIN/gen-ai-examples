mcp_config_sse = {
    "weather_tools": {
        "url": "http://localhost:8000/sse",
        "transport": "sse",
    }
}

mcp_config_stdio = {
    "weather_tools": {
        "command": "python",
        "args": ["aip_agent_quickstart/mcp_servers/mcp_server_stdio.py"],
        "transport": "stdio",
    }
}

mcp_config_arxiv_sse = {
    "arxiv_tools": {
        "url": "http://localhost:8006/YWRtaW46YWRtaW4=/sse",
        "transport": "sse",
    }
}
