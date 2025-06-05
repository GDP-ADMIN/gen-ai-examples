"""Automatic BOSA Twitter tools generator

This file is used to generate BOSA Twitter tools for the agent.

Authors:
    Saul Sayers (saul.sayers@gdplabs.id)
"""

import os
from bosa_connectors import BOSAConnectorToolGenerator

bosa_connector_tool_generator = BOSAConnectorToolGenerator(
    api_base_url=os.getenv("BOSA_API_BASE_URL", "https://api.bosa.id"),
    api_key=os.getenv("BOSA_API_KEY", ""),
    app_name="twitter",
)
BOSA_TWITTER_TOOLS = bosa_connector_tool_generator.generate_tools()