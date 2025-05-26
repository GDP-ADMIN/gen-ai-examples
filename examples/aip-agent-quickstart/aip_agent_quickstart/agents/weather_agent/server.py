"""Weather A2A server for LangGraphAgent.

This server instantiates a LangGraphAgent with weather lookup capabilities and serves it
via the A2A protocol using the to_a2a convenience method.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

import click
import uvicorn
from a2a.types import AgentAuthentication, AgentCapabilities, AgentCard, AgentSkill
from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.utils.logger_manager import LoggerManager
from langchain_openai import ChatOpenAI
from weather_agent import config
from weather_agent.tools import weather_tool

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
    """Runs the LangGraph Weather A2A server."""
    logger.info(f"Starting {config.SERVER_AGENT_NAME} on http://{host}:{port}")

    agent_card = AgentCard(
        name=config.SERVER_AGENT_NAME,
        description=config.AGENT_DESCRIPTION,
        url=f"http://{host}:{port}",
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
        authentication=AgentAuthentication(schemes=["public"]),
        tags=["weather"],
    )

    llm = ChatOpenAI(
        model=config.LLM_MODEL_NAME, temperature=config.LLM_TEMPERATURE, streaming=True
    )
    tools = [weather_tool]

    langgraph_agent = LangGraphAgent(
        name=config.SERVER_AGENT_NAME,
        instruction=config.AGENT_INSTRUCTION,
        model=llm,
        tools=tools,
    )

    app = langgraph_agent.to_a2a(
        agent_card=agent_card,
    )

    logger.info("A2A application configured. Starting Uvicorn server...")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
