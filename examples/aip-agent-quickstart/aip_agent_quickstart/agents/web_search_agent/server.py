"""WebSearchAgent A2A server.

This server instantiates a LangGraphAgent with web_search_agent capabilities and serves it
via the A2A protocol using the to_a2a convenience method.

To be filled by the user.
"""

import click
import uvicorn
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.utils.logger_manager import LoggerManager
from langchain_openai import ChatOpenAI

# Imports from your agent's specific logic package
from web_search_agent import config
from web_search_agent.tools import sample_tool  # Example tool

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
    """Runs the LangGraph WebSearchAgent A2A server."""
    logger.info(f"Starting {config.SERVER_AGENT_NAME} on http://{host}:{port}")

    agent_card = AgentCard(
        name=config.SERVER_AGENT_NAME,
        description=config.AGENT_DESCRIPTION,
        url=f"http://{host}:{port}",  # This should be the publicly accessible URL
        version=config.AGENT_VERSION,
        defaultInputModes=["text"],  # Or other modes like "image", "audio"
        defaultOutputModes=["text"],  # Or other modes
        capabilities=AgentCapabilities(streaming=True),  # Adjust as needed
        skills=[
            AgentSkill(
                id="web_search_agent_skill",
                name="WebSearchAgent Default Skill",
                description="A sample skill for the WebSearchAgent.",
                examples=["What can you do?"],  # Replace with actual examples
                tags=["web_search_agent", "sample"],
            )
        ],
        tags=["web_search_agent"],
    )

    # Configure your LLM (e.g., OpenAI, Anthropic, local model)
    llm = ChatOpenAI(
        model=config.LLM_MODEL_NAME,
        temperature=config.LLM_TEMPERATURE,
        streaming=True,
        # Add other necessary parameters like api_key if not set globally
    )

    tools = [sample_tool]  # Add your agent's tools here

    # Instantiate your agent (e.g., LangGraphAgent or a custom one)
    langgraph_agent = LangGraphAgent(
        name=config.SERVER_AGENT_NAME,
        instruction=config.AGENT_INSTRUCTION,
        model=llm,
        tools=tools,
    )

    # Convert the agent to an A2A FastAPI app
    app = langgraph_agent.to_a2a(
        agent_card=agent_card,
        # You can add more A2A specific configurations here
    )

    logger.info("A2A application configured. Starting Uvicorn server...")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
