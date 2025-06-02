"""Tools for the AIP Agent Quickstart package.

This module provides a centralized import interface for all tools, with clear naming
conventions to distinguish between different frameworks (LangChain, ADK, etc.).

Framework-specific imports:
- LangChain tools: Use 'langchain_' prefix
- ADK tools: Use 'adk_' prefix
- Generic tools: No prefix

Example usage:
    from aip_agent_quickstart.tools import langchain_add_numbers, adk_add_numbers
    from aip_agent_quickstart.tools import langchain_weather_tool, adk_weather_tool
"""

# ruff: noqa: F401
from typing import Union

from langchain.tools import tool

# Import ADK tools
from .adk_arithmetic_tools import add_numbers as adk_add_numbers
from .adk_arithmetic_tools import sum_numbers as adk_sum_numbers
from .adk_weather_tool import weather_tool as adk_weather_tool

# Import LangChain tools
from .langchain_arithmetic_tools import add_numbers as langchain_add_numbers
from .langchain_weather_tool import weather_tool as langchain_weather_tool
from .twitter_bosa_tool import twitter_get_user_tool

# Import generic/standalone tools
from .weather_forecast_tool import get_weather_forecast

# Framework-specific exports
__all__ = [
    # LangChain tools
    "langchain_add_numbers",
    "langchain_weather_tool",
    "twitter_get_user_tool"
    # ADK tools
    "adk_add_numbers",
    "adk_sum_numbers",
    "adk_get_weather",
    "adk_weather_tool",
    # Generic/standalone tools
    "get_weather_forecast",
]
