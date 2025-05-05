"""GLChat Tools MCP by SSE."""

import json

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GLChat Tools")

@mcp.tool()
def message(prompt: str) -> int:
    """Send message to GLChat.

    Args:
        prompt: The prompt.
    Returns:
        str: The response from GLChat.
    """
    url = "https://chat-api.gdplabs.id/message"
    payload = {
        "chatbot_id": "general-purpose",
        "message": prompt,
        'content-type': 'application/json'
    }
    response = requests.post(url, data=payload, stream=True)
    content = response.content.decode('utf-8')
    lines = content.split('\n')

    final_message = ""
    for line in lines:
        if line.startswith('data:'):
            try:
                json_str = line[5:]  # Remove 'data:' prefix
                data = json.loads(json_str)

                if 'message' in data and data['status'] == 'response':
                    final_message = data['message']
            except json.JSONDecodeError:
                # Skip malformed JSON
                continue

    return final_message

if __name__ == "__main__":
    mcp.run(transport="sse")
