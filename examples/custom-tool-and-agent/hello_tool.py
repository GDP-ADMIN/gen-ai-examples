# hello_tool.py
from gllm_agents import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Type

# Optional: Define input schema if the tool needs arguments
class HelloInput(BaseModel):
    name: str = Field(..., description="The name to say hello to")

class SimpleHelloTool(BaseTool):
    """A simple tool that says hello."""
    name: str = "simple_hello_tool"
    description: str = "Greets the user by name."
    args_schema: Type[BaseModel] = HelloInput

    def _run(self, name: str, **kwargs: Any) -> str:
        """Uses the tool."""
        return f"Hello, {name}!"