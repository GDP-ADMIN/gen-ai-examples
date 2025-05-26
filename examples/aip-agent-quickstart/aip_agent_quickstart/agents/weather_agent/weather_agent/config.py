"""Configuration for the Weather Agent.

This module contains configuration constants for the Weather A2A server.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

# Server configuration
SERVER_AGENT_NAME = "WeatherAgent"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8001

# Agent configuration
AGENT_DESCRIPTION = "A weather agent that provides weather information for cities."
AGENT_VERSION = "1.0.0"
AGENT_INSTRUCTION = (
    "You are a weather agent that provides weather information for cities. "
    "Always use the weather_tool for looking up weather data. "
    "Format your responses clearly and professionally."
)

# LLM configuration
LLM_MODEL_NAME = "gpt-4.1"
LLM_TEMPERATURE = 0
