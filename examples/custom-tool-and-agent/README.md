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

## 2. Agent Development Guide

### Creating a Single Agent

Let's create an agent with the following capabilities:
- Get current date and time
- Calculate time difference between two date-time values

We will be using sample tools from the [sample_tools](sample_tools) folder:
- [time_tool.py](sample_tools/time_diff_tool.py) contains a tool to get the current time
- [time_diff_tool.py](sample_tools/time_diff_tool.py) contains a tool to calculate time difference between two date-time values

#### Here's the general workflow for creating an agent in GL Chat:
1. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in GL Chat
2. Select the "Tools" menu and click the "Upload Tool" button
3. Upload the `time_tool.py` and the `time_diff_tool.py` files
4. Upon successful upload, the `custom_time_tool` and the `time_diff_tool` should appear in the "Custom Tools" menu
5. Select the "Agent" menu and click the "Create Agent" button
   <img width="960" alt="image" src="https://github.com/user-attachments/assets/a40d6af6-9731-4547-8610-2e729df03483" />

6. Fill in all the required fields, for example:
   <img width="960" alt="image" src="https://github.com/user-attachments/assets/24fe19db-d284-4ca0-9dc5-a1c6c82caf26" />

   - **Agent Name**: hello_world_agent
   - **Agent Display Name**: Hello World Agent
   - **Description**: New Agent
   - **Model**: gpt-4o
   - **Tools**: `custom_time_tool` and `time_diff_tool`
   - **Sub-Agents**: -
   - **Timeout**: 60
   - **Instructions**:
   ```
   You are an agent that can perform time operations.

   You have the following capabilities:
   - Get current time
   - Calculate time difference between two date-time values

   Always use current_time_tool to get current time before responding to a user's query.
   ```

7. Click the "Save" button
8. Open the [Chatbot menu](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/?chatbot_id=general-purpose) page in GL Chat
9. Click "More Agents" and you should see the newly created "Hello World Agent"
   <img width="518" alt="image" src="https://github.com/user-attachments/assets/c9f0988a-9ee5-4f68-a75d-5e08c46b7367" />
10. You can ask some questions to verify if the agent works as expected
<img width="677" alt="image" src="https://github.com/user-attachments/assets/57da6c3b-6f19-478b-a15c-1a5c9e959fde" />



