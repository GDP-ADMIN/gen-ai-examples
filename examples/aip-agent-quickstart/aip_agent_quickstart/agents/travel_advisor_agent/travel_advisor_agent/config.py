"""Configuration for the TravelAdvisorAgent Agent.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --- Agent Server Configuration ---
SERVER_AGENT_NAME: str = "TravelAdvisorAgent"
DEFAULT_HOST: str = "0.0.0.0"
DEFAULT_PORT: int = 8002
AGENT_VERSION: str = "0.1.0"

# --- LLM Configuration ---
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

LLM_MODEL_NAME: str = "gpt-4.1"
LLM_TEMPERATURE: float = 0.01

# --- Agent Specific Configuration ---
AGENT_DESCRIPTION: str = "An agent that provides a list of recommended places to visit based on user queries."
AGENT_INSTRUCTION: str = (
    "You are the TravelAdvisorAgent. "
    "Your primary function is to recommend places to visit in a specific city. "
    "Use the get_place_recommendations_tool to find suitable places based on the user's requested city. "
    "Be helpful and provide clear, concise recommendations."
)
