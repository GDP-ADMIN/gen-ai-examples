"""Weather A2A server for LangGraphAgent.

This server instantiates a LangGraphAgent with weather lookup capabilities and serves it
via the A2A protocol using the to_a2a convenience method.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

import importlib
import os

import click
import uvicorn
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from gllm_agents.utils.logger_manager import LoggerManager
from weather_agent import config

logger = LoggerManager().get_logger(__name__)


def load_agent(agent_type: str):
    """Dynamically load the agent based on type.

    Args:
        agent_type (str): Type of agent to load ('langgraph' or 'google_adk')

    Returns:
        The loaded agent instance
    """
    module_name = f"{agent_type}_agent"
    try:
        agent_module = importlib.import_module(module_name)
        return getattr(agent_module, f"{agent_type}_agent")
    except (ImportError, AttributeError) as e:
        logger.error(f"Failed to load agent type {agent_type}: {str(e)}")
        raise click.BadParameter(f"Invalid agent type: {agent_type}")


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
@click.option(
    "--agent-type",
    "agent_type",
    default=os.environ.get("framework", "langgraph"),
    type=click.Choice(["langgraph", "google_adk", "langchain"]),
    help="Type of agent to use. Defaults to framework env var, then 'langgraph'.",
    show_default=True,
)
def main(host: str, port: int, agent_type: str) -> None:
    """Runs the Weather A2A server with selected agent type."""
    logger.info(
        f"Starting {config.SERVER_AGENT_NAME} on http://{host}:{port} with {agent_type} agent"
    )

    agent_card = AgentCard(
        name=config.SERVER_AGENT_NAME,
        description=config.AGENT_DESCRIPTION,
        url=config.AGENT_URL,
        version=config.AGENT_VERSION,
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(
                id="weather",
                name="Weather Lookup",
                description="Provides current weather information for cities.",
                examples=["What's the weather in Tokyo?", "Get weather for London"],
                tags=["weather"],
            )
        ],
        tags=["weather"],
    )

    # Load the appropriate agent dynamically
    agent = load_agent(agent_type)

    app = agent.to_a2a(
        agent_card=agent_card,
    )

    logger.info(
        f"A2A application configured with {agent_type} agent. Starting Uvicorn server..."
    )
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
