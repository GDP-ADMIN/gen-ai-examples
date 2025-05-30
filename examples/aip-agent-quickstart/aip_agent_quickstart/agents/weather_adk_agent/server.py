"""WebSearchAgent A2A server.

This server instantiates a Google ADK Weather Agent with weather_agent capabilities and serves it
via the A2A protocol using the to_a2a convenience method.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

import click
import uvicorn
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from gllm_agents.agent.google_adk_agent import GoogleADKAgent
from gllm_agents.utils.logger_manager import LoggerManager

# Imports from your agent's specific logic package
from weather_adk_agent import config
from weather_adk_agent.tools import weather_tool

logger = LoggerManager().get_logger(__name__)


@click.command()
@click.option(
    "--host", "host", default=config.DEFAULT_HOST, help="Host to bind the server to."
)
@click.option(
    "--port",
    "port",
    default=config.DEFAULT_PORT,
    type=int,
    help="Port to bind the server to.",
)
def main(host: str, port: int) -> None:
    """Runs the Google ADK Weather Agent A2A server."""
    logger.info(f"Starting {config.SERVER_AGENT_NAME} on http://{host}:{port}")

    agent_card = AgentCard(
        name=config.SERVER_AGENT_NAME,
        description=config.AGENT_DESCRIPTION,
        url=config.AGENT_URL,
        version=config.AGENT_VERSION,
        defaultInputModes=["text"],  # Or other modes like "image", "audio"
        defaultOutputModes=["text"],  # Or other modes
        capabilities=AgentCapabilities(streaming=True),  # Adjust as needed
        skills=[
            AgentSkill(
                id="web_search_id_1",
                name="WebSearchAgent Default Skill",
                description="This skill enables the WebSearchAgent to perform web searches using the Google Serper API. It can be used to fetch information on a wide range of topics, from general knowledge to specific domains.",
                examples=[
                    "What is the capital of France?",
                    "How does machine learning work?",
                ],  # Actual examples
                tags=["web_search_agent", "information_retrieval"],
            )
        ],
        tags=["web_search_agent"],
    )

    tools = [
        weather_tool,
    ]

    agent = GoogleADKAgent(
        model="gemini-2.0-flash",
        name=config.SERVER_AGENT_NAME,
        description=config.AGENT_DESCRIPTION,
        instruction=config.AGENT_INSTRUCTION,
        tools=tools,
    )

    # Convert the agent to an A2A FastAPI app
    app = agent.to_a2a(
        agent_card=agent_card,
        # You can add more A2A specific configurations here
    )

    logger.info("A2A application configured. Starting Uvicorn server...")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
