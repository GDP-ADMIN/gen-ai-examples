"""Automatic BOSA Twitter tools generator

This file is used to generate BOSA Twitter tools for the agent.

Authors:
    Saul Sayers (saul.sayers@gdplabs.id)
"""

import os
from bosa_connectors import BOSAConnectorToolGenerator
from gllm_agents.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)

BOSA_API_BASE_URL = os.getenv("BOSA_API_BASE_URL", "https://api.bosa.id")
BOSA_API_KEY = os.getenv("BOSA_API_KEY", "")

if not BOSA_API_BASE_URL or not BOSA_API_KEY:
    logger.error("BOSA_API_BASE_URL and BOSA_API_KEY are not set")
    raise ImportError("BOSA_API_BASE_URL and BOSA_API_KEY are not set")

bosa_connector_tool_generator = BOSAConnectorToolGenerator(
    api_base_url=BOSA_API_BASE_URL,
    api_key=BOSA_API_KEY,
    app_name="twitter",
)

bosa_twitter_tools = bosa_connector_tool_generator.generate_tools()