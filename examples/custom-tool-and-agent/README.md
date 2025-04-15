# Custom Tool and Agent Hello World
This is an example how to create custom tool and agent.

## 1. Tool Development Guide

### Creating Basic Tools with the Decorator

The simplest way to create a new tool is using the `@tool_plugin` decorator:

```python
from typing import Any
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from gdplabs_gen_ai_starter_gllm_backend.gllm_agents.plugins import tool_plugin

# Input schema definition
class GreetingInput(BaseModel):
    """Input schema for the greeting tool."""
    name: str = Field(..., description="Name to greet")

# Tool implementation with decorator
@tool_plugin(version="1.0.0")
class GreetingTool(BaseTool):
    """A simple greeting tool implementation."""

    name: str = "greeting"
    description: str = "Generates a greeting message for the provided name"
    args_schema: type[BaseModel] = GreetingInput

    # Core method for any tool which implements the tool's functionality
    def _run(self, name: str, **kwargs: Any) -> str:
        """Run the greeting tool."""
        return f"Hello, {name}! Welcome to the tool plugin system."
```

This pattern enables a clean, declarative style for tool creation with minimal boilerplate.

### Upload tool to GL Chat
1. Create a custom tool using the decorator as defined previously and save it as a Python (.py) file
2. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in GL Chat
3. Select the "Tools" menu and click the "Upload Tool" button
<img width="960" alt="image" src="https://github.com/user-attachments/assets/90d0b2fa-b481-4f56-a90e-c2f0c0340f41" />

4. Upload your newly created tool
<img width="960" alt="image" src="https://github.com/user-attachments/assets/154685cf-7415-4b07-ac9d-d4db3588f7c2" />

5. Upon successful upload, your tool should appear in the "Custom Tools" menu
<img width="960" alt="image" src="https://github.com/user-attachments/assets/c71fcf6c-655f-4efb-a57c-4703d7ba4513" />

