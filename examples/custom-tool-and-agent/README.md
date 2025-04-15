# Custom Tool and Agent Hello World
This is an example how to create custom tool and agent.

## Pre-requisites

1. **Python v3.11 or above**:
   - Ensure that Python is installed and available in your environment.

2. **[Poetry](https://python-poetry.org/docs/) v1.8.1 or above**:
   - Poetry is used for dependency management and packaging in Python projects. It simplifies the process of managing project dependencies and virtual environments.


3. **SSH Key in your GitHub Account**

   You must add your SSH key to your GitHub account. Please follow this instruction by GitHub: [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account). This is required as this sample has dependency to a private GitHub repository.

4. **VSCode IDE**
   - Go to [VSCode](https://code.visualstudio.com/download) to download VSCode IDE.
  
5. **GDP Labs VPN**
   - The GDP Labs VPN is required to access Gloria staging environment 

### Installing dependencies

1. Clone the `gen-ai-examples` repository
```bash
git clone git@github.com:GDP-ADMIN/gen-ai-examples.git
```
2. Navigate to the `custom-tool-and-agent` directory
3. Install all dependencies specified in the lock file
```bash
poetry install
```

## Tool Development Guide

### Creating Basic Tools with the Decorator
1. Open your VSCode
2. Activate the newly installed virtual environment
3. Create a new Python (`.py`) file
4. The simplest way to create a new tool is using the `@tool_plugin` decorator:

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
   Copy the above code in your newly created Python file
5. Check the import statements, ensure that there's no import error

### Upload tool to GL Chat
1. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in Gloria
2. Select the "Tools" menu and click the "Upload Tool" button
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/90d0b2fa-b481-4f56-a90e-c2f0c0340f41" />

3. Upload your newly created tool
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/154685cf-7415-4b07-ac9d-d4db3588f7c2" />

4. Upon successful upload, your tool should appear in the "Custom Tools" menu
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/c71fcf6c-655f-4efb-a57c-4703d7ba4513" />

## Agent Development Guide

### Creating a Single Agent

Let's create an agent with the following capabilities:
- Get current date and time
- Calculate time difference between two date-time values

We will be using sample tools from the [sample_tools](sample_tools) folder:
- [time_tool.py](sample_tools/time_diff_tool.py) contains a tool to get the current time
- [time_diff_tool.py](sample_tools/time_diff_tool.py) contains a tool to calculate time difference between two date-time values

#### Here's the general workflow for creating an agent in GL Chat:
1. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in Gloria
2. Select the "Tools" menu and click the "Upload Tool" button
3. Upload the `time_tool.py` and the `time_diff_tool.py` files
4. Upon successful upload, the `custom_time_tool` and the `time_diff_tool` should appear in the "Custom Tools" menu
5. Select the "Agent" menu and click the "Create Agent" button
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/a40d6af6-9731-4547-8610-2e729df03483" />

6. Fill in all the required fields, for example:
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/c5eff957-b6ef-4956-8de9-2cff1792f12b" />

   - **Agent Name**: timer_agent
   - **Agent Display Name**: Timer Agent
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

   Always use custom_time_tool to get current time before responding to a user's query.
   ```
   **Note**: Since we are creating a single agent, leave the Sub-Agents field empty.

7. Click the "Save" button
8. Upon successful creation, the Timer Agent should appear in the "Custom Agents" menu

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/c22a0299-6385-48a9-90b9-5e52c85258f5" />

### Testing - Converse with Agent

Since we can't yet deploy the newly created agent directly to Gloria, we provide a template agent that you can edit according to your custom agent, in this case the Timer Agent. The template agent is named Hello World Agent.

1. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in Gloria
2. Select "Custom Agent"
3. Select triple dots icon on the Hello World Agent card and then click "Edit"

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/663c3775-6e39-4747-ba2e-1e841b6c0c99" />
   
4. Fill in all fields according to our newly created Timer Agent, except for the **Agent Name** field

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/28dc98c2-83db-4cfc-9311-7dc167e722d8" />

5. Click "Save"
6. Open the [Chatbot menu](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/?chatbot_id=general-purpose) page in Gloria
7. In the Chatbot Selection, select "Demo General Purpose"

<img width="443" alt="image" src="https://github.com/user-attachments/assets/053a5ca4-d387-4595-a14e-46c04c440ef6" />

8. Select the "More Agents" and scroll down, you should see the "Timer Agent"

<img width="536" alt="image" src="https://github.com/user-attachments/assets/06b815c8-8131-462b-b126-28800b833ee3" />

9. Ask a question to the Timer Agent

<img width="744" alt="image" src="https://github.com/user-attachments/assets/aa75d5f3-fe97-4f34-8c4a-80397cd765bc" />

