mcp_config_sse = {
    "math_tools": {
        "url": "http://localhost:8000/sse",
        "transport": "sse",
    }
}

mcp_config_stdio = {
    "math_tools": {
        "command": "python",
        "args": ["mcp_tools/math_tools_stdio.py"],
        "transport": "stdio",
    }
}
