"""Example showing Google ADK agent with MCP tools integration using SSE transport.

Authors:
    Fachriza Dian Adhiatma (fachriza.d.adhiatma@gdplabs.id)
"""

from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.examples.mcp_configs.configs import mcp_config_sse

from aip_agent_quickstart.config import DEFAULT_AGENT_INSTRUCTION

if __name__ == "__main__":
    agent = GoogleADKAgent(
        name="ADK_SSE_Weather_Agent",
        instruction=DEFAULT_AGENT_INSTRUCTION,
        model="gemini-2.0-flash",
    )
    agent.add_mcp_server(mcp_config_sse)

    response = agent.run(query="What's the weather forecast for monday?")
    print(f"Response: {response.get('output')}")
