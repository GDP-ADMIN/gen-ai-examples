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
        GDPLABS_OVERTIME_ASSISTANT (str): The agent type for GDP Labs Overtime
        HELP_CENTER_CATAPA (str): The agent type for Help Center Catapa.
        REGULATION (str): The agent type for Regulation.
    """

    DATA_ANALYST = "data_analyst"
    ESS_ASSISTANT = "ess_assistant"
    GDPLABS_OVERTIME_ASSISTANT = "gdplabs_overtime_assistant"
    HELP_CENTER_CATAPA = "help_center_catapa"
    REGULATION = "regulation"


PUBLIC_AGENT_TYPES = [
    AgentType.HELP_CENTER_CATAPA.value,
    AgentType.REGULATION.value,
]
