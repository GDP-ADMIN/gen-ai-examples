"""GLChat Tools MCP by STDIO."""

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
    response = requests.post(
        "https://chat-api.gdplabs.id/message",
        data={'chatbot_id': 'general-purpose', 'message': prompt, 'content-type': 'application/json'}
    )
    
    final_message = ""
    for line in response.content.decode('utf-8').split('\n'):
        if line.startswith('data:'):
            try:
                data = json.loads(line[5:])
                if data.get('status') == 'response' and 'message' in data:
                    final_message = data['message']
            except json.JSONDecodeError:
                pass
    
    return final_message

if __name__ == "__main__":
    mcp.run(transport="stdio")
