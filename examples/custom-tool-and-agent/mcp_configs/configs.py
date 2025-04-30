mcp_config_sse = {
    "text_frequency_counter": {
        "url": "http://localhost:8000/sse",
        "transport": "sse",
    }
}

mcp_config_stdio = {
    "text_frequency_counter": {
        "command": "python",
        "args": ["mcp_tools/text_frequency_counter_stdio.py"],
        "transport": "stdio",
    }
}
