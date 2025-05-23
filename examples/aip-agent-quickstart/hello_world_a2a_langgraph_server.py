"""Example A2A server for a LangGraphAgent Weather Service.

This server instantiates a LangGraphAgent with weather lookup capabilities and serves it
via the A2A protocol using the to_a2a convenience method.

It will listen on http://localhost:8001 by default.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

import click
import uvicorn
from a2a.types import AgentAuthentication, AgentCapabilities, AgentCard, AgentSkill
from langchain_openai import ChatOpenAI

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.utils.logger_manager import LoggerManager
from gllm_agents.examples.tools import weather_tool

logger = LoggerManager().get_logger(__name__)


SERVER_AGENT_NAME = "WeatherAgent"


@click.command()
@click.option("--host", "host", default="localhost", help="Host to bind the server to.")
@click.option("--port", "port", default=8001, help="Port to bind the server to.")
def main(host: str, port: int):
    """Runs the LangGraph Weather A2A server."""
    logger.info(f"Starting {SERVER_AGENT_NAME} on http://{host}:{port}")

    agent_card = AgentCard(
        name=SERVER_AGENT_NAME,
        description="A weather agent that provides weather information for cities.",
        url=f"http://{host}:{port}",
        version="1.0.0",
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

    llm = ChatOpenAI(model="gpt-4.1", temperature=0, streaming=True)
    tools = [weather_tool]

    langgraph_agent = LangGraphAgent(
        name=SERVER_AGENT_NAME,
        instruction="You are a weather agent that provides weather information for cities. Always use the weather_tool for looking up weather data. Format your responses clearly and professionally.",
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
