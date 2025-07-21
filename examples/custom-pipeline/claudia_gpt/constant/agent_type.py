"""Module for defining the agent type.

This module contains the definition of the agent type enumeration.

Authors:
    Immanuel Rhesa (immanuel.rhesa@gdplabs.id)
"""

from enum import Enum


class AgentType(Enum):
    """Enumeration for the agent type.

    Attributes:
        DATA_ANALYST (str): The agent type for Data Analyst.
        ESS_ASSISTANT (str): The agent type for ESS Assistant.
        HELP_CENTER_CATAPA (str): The agent type for Help Center Catapa.
        REGULATION (str): The agent type for Regulation.
        NLWEB (str): The agent type for NLWeb.
        MCP (str): The agent type for MCP.
    """

    DATA_ANALYST = "data_analyst"
    ESS_ASSISTANT = "ess_assistant"
    HELP_CENTER_CATAPA = "help_center_catapa"
    REGULATION = "regulation"
    NLWEB = "nlweb"
    MCP = "mcp"


PUBLIC_AGENT_TYPES = [
    AgentType.HELP_CENTER_CATAPA.value,
    AgentType.REGULATION.value,
    AgentType.NLWEB.value,
    AgentType.MCP.value,
]
