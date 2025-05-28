# This makes `web_search_agent` a Python package.

# You can expose parts of your agent's internal modules here if desired.
# For example, to make config directly importable as `from web_search_agent import config`:
from . import config
from . import tools

# Or specifically expose variables/functions:
# from .config import DEFAULT_PORT, AGENT_DESCRIPTION
# from .tools import sample_tool

__all__ = [
    "config",
    "tools",
    # Add other modules or specific variables/functions you want to expose
]
