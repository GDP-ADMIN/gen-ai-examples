"""Example showing Google ADK agent with MCP tools integration using stdio transport.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from aip_agent_quickstart.mcp_configs.configs import mcp_config_stdio

if __name__ == "__main__":
    agent = GoogleADKAgent(
        name="ADK_Stdio_Weather_Agent_Stream",
        instruction="You are a helpful assistant that can provide weather forecasts. For weather, specify the day in lowercase (e.g., 'monday').",
        model="gemini-2.0-flash",
    )
    agent.add_mcp_server(mcp_config_stdio)

    response = agent.run(query="What's the weather forecast for monday?")
    print(f"Response: {response.get('output')}")
