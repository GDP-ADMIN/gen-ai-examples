"""Weather A2A server for LangGraphAgent.

This server instantiates a LangGraphAgent with weather lookup capabilities and serves it
via the A2A protocol using the to_a2a convenience method.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.agent.langgraph_agent import LangGraphAgent
from gllm_agents.utils.logger_manager import LoggerManager
from langchain_openai import ChatOpenAI

from weather_agent import config
from weather_agent.tools import langchain_weather_tool

logger = LoggerManager().get_logger(__name__)


llm = ChatOpenAI(
    model=config.LLM_MODEL_NAME, temperature=config.LLM_TEMPERATURE, streaming=True
)
tools = [langchain_weather_tool]

langgraph_agent = LangGraphAgent(
    name=config.SERVER_AGENT_NAME,
    instruction=config.AGENT_INSTRUCTION,
    model=llm,
    tools=tools,
)
logger.info(f"LangGraph Agent with name {config.SERVER_AGENT_NAME} created")
