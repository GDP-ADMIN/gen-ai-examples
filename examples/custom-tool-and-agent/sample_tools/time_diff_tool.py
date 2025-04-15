from datetime import datetime
from typing import Any, Literal
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from gdplabs_gen_ai_starter_gllm_backend.gllm_agents.plugins import tool_plugin

# Input schema definition
class TimeDiffInput(BaseModel):
    """Input schema for the time diff tool."""
    date1: str = Field(..., description="First datetime string")
    date2: str = Field(..., description="Second datetime string")
    unit: Literal["years", "months"] = Field(default="years", description="Unit for difference: 'years' or 'months'")

# Tool implementation with decorator
@tool_plugin(version="1.0.0")
class TimeDiffTool(BaseTool):
    """A tool to calculate the difference between two dates in years or months."""

    name: str = "time_diff_tool"
    description: str = "Calculates the difference between two dates in years or months."
    args_schema: type[BaseModel] = TimeDiffInput

    # Core method for any tool which implements the tool's functionality
    def _run(self, date1: str, date2: str, unit: str = "years", **kwargs: Any) -> str:
        """Run the time diff tool."""
        try:
            dt1 = datetime.strptime(date1, "%m/%d/%y %H:%M:%S")
            dt2 = datetime.strptime(date2, "%m/%d/%y %H:%M:%S")
            if unit == "years":
                diff = abs(dt1.year - dt2.year)
                # Adjust if dt1's month/day is before dt2's
                if (dt1.month, dt1.day) < (dt2.month, dt2.day):
                    diff -= 1
                return f"Difference: {diff} years"
            elif unit == "months":
                diff = abs((dt1.year - dt2.year) * 12 + (dt1.month - dt2.month))
                # Adjust if dt1's day is before dt2's
                if dt1.day < dt2.day:
                    diff -= 1
                return f"Difference: {diff} months"
            else:
                return "Invalid unit. Use 'years' or 'months'."
        except Exception as e:
            return f"Error: {e}"