"""Research Agent A2A Server.

This module implements an A2A server for the Research Agent that can handle academic
and travel-related queries using MCP servers and A2A agents.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

import click
from typing import Optional

from a2a.types import AgentAuthentication, AgentCapabilities, AgentCard, AgentSkill
from a2a.server import A2AServer, ServeConfig
from gllm_agents.utils.logger_manager import LoggerManager
from pydantic import BaseModel, Field

from research_agent.agent import create_research_agent
from research_agent.config import (
    SERVER_AGENT_NAME,
    AGENT_DESCRIPTION,
    AGENT_VERSION,
    AGENT_INSTRUCTION,
    DEFAULT_HOST,
    DEFAULT_PORT,
)

logger = LoggerManager().get_logger(__name__)


class QueryRequest(BaseModel):
    """Request model for the research agent query."""

    query: str = Field(..., description="The query to process")
    conversation_id: Optional[str] = Field(
        None, description="Optional conversation ID for multi-turn conversations"
    )


class QueryResponse(BaseModel):
    """Response model for the research agent query."""

    response: str = Field(..., description="The agent's response")
    conversation_id: Optional[str] = Field(
        None, description="The conversation ID for multi-turn conversations"
    )


async def process_query(query: str) -> str:
    """Process a query using the research agent.

    Args:
        query: The user's query

    Returns:
        The agent's response
    """
    try:
        # Create a new agent instance for this query
        agent = create_research_agent()

        # Process the query
        response = await agent.ainvoke({"messages": [("user", query)]})

        # Extract and return the response
        if hasattr(response, "get") and "messages" in response:
            return (
                response["messages"][-1].content
                if response["messages"]
                else "No response generated"
            )
        elif hasattr(response, "content"):
            return response.content
        else:
            return str(response)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return f"An error occurred while processing your request: {str(e)}"


@click.command()
@click.option(
    "--host", "host", default=DEFAULT_HOST, help="Host to bind the server to."
)
@click.option(
    "--port",
    "port",
    default=DEFAULT_PORT,
    type=int,
    help="Port to bind the server to.",
)
def main(host: str, port: int) -> None:
    """Runs the LangGraph Research A2A server."""
    logger.info(f"Starting {SERVER_AGENT_NAME} on http://{host}:{port}")

    # Create the agent instance
    agent = create_research_agent()

    # Set up the A2A server
    server = A2AServer(
        agent=agent,
        config=ServeConfig(
            host=host,
            port=port,
            agent_card=AgentCard(
                name=SERVER_AGENT_NAME,
                description=AGENT_DESCRIPTION,
                url=f"http://{host}:{port}",
                version=AGENT_VERSION,
                defaultInputModes=["text"],
                authentication=AgentAuthentication(type="none"),
                capabilities=AgentCapabilities(
                    text_input=True,
                    text_output=True,
                ),
                skills=[
                    AgentSkill(
                        name="research",
                        description="Perform research on academic and travel-related topics",
                    )
                ],
                instruction=AGENT_INSTRUCTION,
            ),
            log_level="info",
        ),
    )

    # Run the server
    server.run()


if __name__ == "__main__":
    main()
