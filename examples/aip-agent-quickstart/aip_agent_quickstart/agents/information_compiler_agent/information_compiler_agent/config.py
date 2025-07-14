"""Configuration for the InformationCompilerAgent Agent."""

import os

from dotenv import load_dotenv

load_dotenv()

# --- Agent Server Configuration ---
SERVER_AGENT_NAME: str = "InformationCompilerAgent"  # Used in AgentCard and logging
DEFAULT_HOST: str = "0.0.0.0"
DEFAULT_PORT: int = 8002
AGENT_VERSION: str = "0.1.0"
AGENT_URL: str = os.getenv("AGENT_URL", "http://localhost:8002")

# --- LLM Configuration ---
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
# ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")

LLM_MODEL_NAME: str = "gpt-4.1"
LLM_TEMPERATURE: float = 0.1

# --- Agent Specific Configuration ---
AGENT_DESCRIPTION: str = (
    "An information compiler agent that helps users organize and manage information in markdown files. "
    "It can read existing markdown files, write new content, create new markdown files, and compile information from various sources into well-structured markdown documents."
)
AGENT_INSTRUCTION: str = (
    "You are the InformationCompilerAgent, a specialized agent for managing information in markdown format. "
    "Your primary functions are to: "
    "1. Read and analyze existing markdown files using the read_markdown_file tool "
    "2. Write and update markdown content using the write_markdown_file tool "
    "3. Create new markdown files when needed using the create_markdown_file tool "
    "4. Help users organize, compile, and structure information in markdown format "
    "Always use the appropriate markdown tools for file operations. "
    "Format your responses clearly and ensure markdown files are well-structured with proper headings, lists, and formatting. "
    "When creating or updating files, consider the existing content and maintain consistency in formatting and organization. "
    "When compiling information into markdown files, always include any provided links or URLs using proper markdown link syntax [text](url) to preserve source references and enable easy navigation."
)
