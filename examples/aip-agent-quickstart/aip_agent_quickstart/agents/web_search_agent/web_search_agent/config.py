"""Configuration for the WebSearchAgent Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Agent Server Configuration ---
SERVER_AGENT_NAME: str = "WebSearchAgent"  # Used in AgentCard and logging
DEFAULT_HOST: str = "0.0.0.0"
DEFAULT_PORT: int = 8002
AGENT_VERSION: str = "0.1.0"

# --- LLM Configuration ---
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
# ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")

LLM_MODEL_NAME: str = "gpt-4.1"
LLM_TEMPERATURE: float = 0.1

# --- Agent Specific Configuration ---
AGENT_DESCRIPTION: str = (
    "A template agent for A2A. (TODO: Replace with actual description)"
)
AGENT_INSTRUCTION: str = (
    "You are the WebSearchAgent Agent. "
    "Your primary function is to (TODO: define your agent's main goal). "
    "Be helpful and concise."
)
