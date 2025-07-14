"""WebSearchAgent A2A server.

This server instantiates a Google ADK Weather Agent with weather_agent capabilities and serves it
via the A2A protocol using the to_a2a convenience method.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent import GoogleADKAgent
from gllm_agents.utils.logger_manager import LoggerManager

# Imports from your agent's specific logic package
from weather_agent import config
from weather_agent.tools import google_adk_weather_tool

logger = LoggerManager().get_logger(__name__)

tools = [
    google_adk_weather_tool,
]

google_adk_agent = GoogleADKAgent(
    model="gemini-2.0-flash",
    name=config.SERVER_AGENT_NAME,
    description=config.AGENT_DESCRIPTION,
    instruction=config.AGENT_INSTRUCTION,
    tools=tools,
)

logger.info(f"Google ADK Agent with name {config.SERVER_AGENT_NAME} created")
