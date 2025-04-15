from datetime import datetime, timezone
from langchain_core.tools import BaseTool
from gllm_plugin.tools import tool_plugin

# Tool implementation with decorator
@tool_plugin(version="1.0.0")
class CustomTimeTool(BaseTool):
    """A simple tool to get a datetime."""

    name: str = "custom_time_tool"
    description: str = "Generates a datetime string in the specified format."

    # Core method for any tool which implements the tool's functionality
    def _run(self) -> str:
        """Run the time tool."""
        try:
            return datetime.now(timezone.utc).strftime("%m/%d/%y %H:%M:%S")
        except Exception as e:
            return f"Invalid date format: {e}"