# Custom Tool and Agent Hello World
This is an example how to create custom tool and agent.

## Prerequisites

<details><summary>Click to expand prerequisites</summary>

This example requires:
- Python Environment
- Access to the specified GitHub repositories 

You need to have proper GitHub authentication configured to access the repositories for pip installation.
</details>

---

## Approach 1: Using Code (Command Line / SDK)

This approach uses the `gllm-agents` library directly in Python.

### Installation

```bash
# From the activated custom-tool-agent-hello-world conda environment
pip install gllm-agents-binary==0.0.1b5
```

### Hello World Example

This example uses two files: `hello_tool.py` for the tool definition and `hello_agent_example.py` to run the agent.

**1. Tool Definition (`hello_tool.py`)**

```python
# hello_tool.py
from gllm_agents import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Type

class HelloInput(BaseModel):
    name: str = Field(..., description="The name to say hello to")

class SimpleHelloTool(BaseTool):
    """A simple tool that says hello."""
    name: str = "simple_hello_tool"
    description: str = "Greets the user by name."
    args_schema: Type[BaseModel] = HelloInput

    def _run(self, name: str, **kwargs: Any) -> str:
        return f"Good day, {name}!"
```

**2. Agent Runner Script (`hello_agent_example.py`)**

```python
# hello_agent_example.py
from gllm_agents import Agent
from langchain_openai import ChatOpenAI
from hello_tool import SimpleHelloTool

# Initialize components
llm = ChatOpenAI(model="gpt-4o")
tool = SimpleHelloTool()

# Create Agent
agent = Agent(
    name="HelloAgent",
    instruction="You are a helpful assistant that can greet people by name using the provided tool.",
    llm=llm,
    tools=[tool],
    verbose=True
)

# Run Agent
query = "Please greet World"
response = agent.run(query)
print(response['output'])
```

### Running the Example & Expected Output

First, set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```

Then run the script:
```bash
python hello_agent_example.py
```

With `verbose=True`, you'll see the agent's thinking process, similar to:
```
> Entering new AgentExecutor chain...
Invoking: `simple_hello_tool` with `{'name': 'World'}`

Hello, World!

> Finished chain.
Hello, World!
```

The key indicators of success:
- The agent initialization completes without errors
- The verbose output shows the tool being invoked
- The final output includes the greeting with "Hello, World!"

--- 

## Approach 2: Using GLChat UI (Web Interface)

This approach involves creating, managing, and testing your tools and agents directly within the GLChat web interface.

### Installation

```bash
# From the activated custom-tool-agent-hello-world conda environment
pip install gllm-plugin-binary==0.0.5
# If you want to use both approaches, also install:
pip install gllm-agents-binary==0.0.1b5
```

### Tool Development via GLChat UI

### Creating a Custom Tool
1. Open your VSCode within the `gen-ai-examples/examples/custom-tool-and-agent` directory.
2. You can create your own tool following guide on the [Advanced: Developing Your Own Custom Tool](#advanced-developing-your-own-custom-tool) section. But, for simplicity, let's use sample tool [weather_forecast_tool.py](./sample_tools/weather_forecast_tool.py).
   *   The sample file demonstrates the basic structure of a tool using the `@tool_plugin` decorator.
   *   **What this tool does**: This sample tool provides weather forecasts for specific days of the week across multiple cities (New York, London, and Tokyo). It uses mock weather data stored within the tool itself and takes a day of the week as input. The tool returns formatted weather information including condition, temperature, and humidity for each location.
3. Open the `weather_forecast_tool.py` file in VSCode.
4. Check the import statements. Ensure that there are no import errors.
   *   **What are import errors?** These errors mean that Python cannot find a specific piece of code (a library or module) that the tool needs to function. This usually happens if a required dependency wasn't installed correctly or if VSCode isn't using the correct Python environment where the dependencies were installed.
   *   **How to check**: Look for any red squiggly underlines beneath `import` statements (like `from gllm_plugin.tools import tool_plugin`) in the VSCode editor. These visual cues indicate a problem. You can also open the "Problems" panel in VSCode (usually accessible via the View menu or by clicking the error/warning icons in the bottom status bar) to see a list of specific errors.
   *   If you see import errors, double-check that you have activated the correct virtual environment (Step 2 - verify the Python interpreter in the status bar) and the script `local-start` (Step 4 under [Running the Code](#running-the-code)) completed without errors.
   *   Once you've successfully run through this example, see the [Advanced: Developing Your Own Custom Tool](#advanced-developing-your-own-custom-tool) section at the end of this document for guidance on creating tools beyond this sample.

### Upload tool to GLChat
1. Open your browser and navigate to the [GLChat login page](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/).
2. Log in using your credentials (e.g., Sign in with Google).

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/13f114ac-1f22-4195-8294-37d498d669fe" />

4. After logging in, click on the "Admin Dashboard" button.

    <img width="960" alt="image" src="https://github.com/user-attachments/assets/29217848-33a4-4010-8d21-43cb6c4f7258" />

5. In the Admin Dashboard, locate the "AI Agent" section in the left sidebar and click on "[Tools](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin/ai-agent/tools)".

    <img width="240" alt="image" src="https://github.com/user-attachments/assets/fd451432-1766-4c19-af51-de78c3b0ef01" />

6. Click the "Upload Tool" button.

    <img width="960" alt="image" src="https://github.com/user-attachments/assets/2221f498-9d6a-40fb-b298-e2f26147a57f" />

7. Upload the `weather_forecast_tool.py` file you created/copied.

    <img width="960" alt="image" src="https://github.com/user-attachments/assets/7c39ec3a-7760-476d-a105-133322c1e823" />

4. Upon successful upload, your tool should appear in the "Custom Tools" menu. A confirmation message will also be displayed indicating that your tool has been successfully registered in the GLChat.
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/2f4ec7e3-0b82-4748-a492-49c8ecbbf5c7" />

### Testing and Validating the Tool

*This section is a work in progress. Steps for specifically testing and validating an uploaded tool before associating it with an agent will be added in a future update.*

### Agent Development Guide

#### Creating a Single Agent

Agent can only use tools that have been registered. If you already have a tool that has not yet been registered, please refer to the [Tool Development Guide](#tool-development-guide) section.

Let's create an agent with the ability to make weather forecasts using the tool we registered in the previous step.

#### Here's the general workflow for creating an agent in GLChat:
1. Login to GLChat Admin Dashboard, refer to [Upload tool to GLChat](#upload-tool-to-glchat) section for details.
2. From the Admin Dashboard, navigate to the "AI Agent" section in the left sidebar and click on "[Agent](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin/ai-agent/agent)".

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/3db6de93-eca1-4313-8deb-14cc1571a5fd" />

3. Click the "Create Agent" button.
4. Fill in all the required fields, for example:

   - **Agent Name**: weather_forecast_agent
   - **Agent Display Name**: Weather Forecast Agent
   - **Description**: This is a weather forecast agent
   - **Model**: gpt-4o
   - **Tools**: `weather_forecast_tool` (Select the tool you uploaded)
   - **Sub-Agents**: -
   - **Timeout**: 60
   - **Instructions**:
     
      ```
      You are an agent that can make a weather forecast prediction.
   
      You are provided with tools to help you make a weather forecast.
      Always use the provided tools when make a weather forecast, do not assume or make up your own answer.
      ```
      
   **Note**: Since we are creating a single agent, leave the Sub-Agents field empty.

      <img width="960" alt="image" src="https://github.com/user-attachments/assets/c048e5a9-d677-400a-b456-f18488d554e9" />

5. Click the "Save" button
6. Upon successful creation, the Weather Forecast Agent should appear in the "Custom Agents" menu

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/17507b12-a25c-4b6e-9758-faceded4184c" />

### Testing the Agent

Since direct deployment/assignment of newly created custom agents to chatbots in GLChat is not yet available (pending the Admin Dashboard feature), we provide a workaround using a pre-existing dummy agent named "Hello World Agent" that is already assigned to the "Demo General Purpose" chatbot in the **staging** environment. We will edit this existing agent to use our custom tool and instructions.

### Configure the Test Agent

1. Navigate back to the GLChat Admin Dashboard (ensure you are still logged in).
2. In the Admin Dashboard, locate the "AI Agent" section in the left sidebar and click on "Agent".
3. Select the "Agent" tab (it might be selected by default) and ensure "Custom Agent" is selected in the filter/dropdown.
4. Find the "Hello World Agent" card, click the triple dots icon (...), and then click "Edit".

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/c3d1b895-dd1b-47d2-b135-b1f4d47ff662" />

5. Fill in all fields according to the Weather Forecast Agent you defined previously (**except** for the **Agent Name** field).
   *   **Notes**: The field `Agent Name` is non-editable and it must remain `hello_world_agent` because this specific name is pre-assigned to the "Demo General Purpose" chatbot for testing purposes.
   *   Update the `Description`, `Model`, `Tools` (select `weather_forecast_tool`), `Timeout`, and `Instructions` to match your Weather Forecast Agent created previously in the [Creating a Single Agent](#creating-a-single-agent).

         <img width="960" alt="image" src="https://github.com/user-attachments/assets/9febd8eb-311b-421b-b2ef-195c8ddcdf1e" />

6. Click "Save".

### Converse with Agent

1. Open the [GLChat Chat UI](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/) in your browser.

   **Tips:**
   If you are on the [Admin Dashboard](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin/knowledge-base) page, you can easily switch to the GLoria Chatbot UI by clicking your profile section at the bottom left of the page and selecting "Switch to GLoria Chatbot".

   <img width="191" alt="image" src="https://github.com/user-attachments/assets/5a4c5e2c-55f6-4269-9e11-b03f3734a3a5" />
   
3. From the left-hand sidebar, click on the "Chatbot" selection menu (it might initially say "Demo General Purpose").
4. Select "Demo General Purpose" from the dropdown list (this chatbot exists in the **staging** environment).

   <img width="443" alt="image" src="https://github.com/user-attachments/assets/053a5ca4-d387-4595-a14e-46c04c440ef6" />

5. In the chat interface, click the "More Agents" button. Scroll down, and you should see the "Hello World Agent" (which is the edited "Hello World Agent" with your settings).

    <img width="516" alt="image" src="https://github.com/user-attachments/assets/3ef050a9-88e0-418b-bb94-90f56d07b219" />

6. Select the "Hello World Agent" and ask it a question, like "What is the weather forecast for Tuesday?".

    <img width="689" alt="image" src="https://github.com/user-attachments/assets/9f52bfd6-0d9d-4e27-90e4-80068d96c34a" />

### Cleanup The Agent

After you successfully test the Weather Forecast Agent, it's better to clean up your work so that others can test it with a clean state.

> [!NOTE]
> As of now, all agents and tools are shared across all users in GLChat. We are still working on Role-Based Access Control (RBAC). That's why we still need this cleanup step.

#### Reset Hello World Agent

1.   Navigate back to the GLChat Admin Dashboard.
2.   In the Admin Dashboard, locate the "AI Agent" section in the left sidebar and click on "Agent".
3.   Find the "Hello World Agent" (which you previously edited), click the triple dots icon, and then click "Edit".

      <img width="960" alt="image" src="https://github.com/user-attachments/assets/c3d1b895-dd1b-47d2-b135-b1f4d47ff662" />

4.   Update the fields back to their original values:

      *    **Agent Display Name**: `Hello World Agent`
      *    **Description**: `Please fill in the Description`
      *   **Model**: `gpt-4o`
      *   **Tools**: Select `time_tool` (remove any other tools)
      *   **Sub-Agents**: Ensure none are selected
      *   **Timeout**: `60`
      *   **Instructions**: `Please fill in the Instruction`
     
6.   Click "Save"

#### Delete The Weather Forecast Agent

1.   Navigate back to the GLChat Admin Dashboard.
2.   In the Admin Dashboard, locate the "AI Agent" section in the left sidebar and click on "Agent".
3.   Find the agent named "Weather Forecast Agent", click the triple dots icon, and then click "Delete".
4.   Make sure the agent is deleted in the UI.

#### Delete the `weather_forecast_tool`

1.   Navigate back to the GLChat Admin Dashboard.
2.   In the Admin Dashboard, locate the "AI Agent\" section in the left sidebar and click on \"Tools\".
3.   Select the \"Custom Tools\" section.
4.   Navigate to the `weather_forecast_tool`, click the triple dots, and then click "Delete".

      <img width="957" alt="image" src="https://github.com/user-attachments/assets/92c8cb42-5192-427f-84bb-bba05a296e96" />
5.   Make sure the tool is deleted in the UI.

## Advanced: Developing Your Own Custom Tool

The steps above guide you through using the provided `weather_forecast_tool.py` sample. To create your *own* custom tool, follow these general principles:

1.  **Create a Python File**: Create a new `.py` file for your tool (e.g., `my_calculator_tool.py`).
2.  **Import Necessary Modules**: You'll typically need `BaseTool` from `gllm_agents`, `BaseModel` and `Field` from `pydantic`, and the `tool_plugin` decorator from `gllm_plugin.tools`.
3.  **Define Input Schema (if needed)**: If your tool requires specific inputs, define a Pydantic `BaseModel` subclass. Use `Field` to add descriptions and validation for each input parameter.

    ```python
    from pydantic import BaseModel, Field

    class MyToolInput(BaseModel):
        parameter1: str = Field(..., description="Description for parameter 1")
        parameter2: int = Field(..., description="Description for parameter 2")
    ```
    
5.  **Create Tool Class**: Define a class that inherits from `gllm_agents.BaseTool`.
6.  **Add Decorator**: Apply the `@tool_plugin(version="...")` decorator to your class for automatic registration.
7.  **Set Class Attributes**: Define the required attributes within your class:
    *   `name`: A unique string identifier for your tool (e.g., `"my_calculator"`).
    *   `description`: A clear, concise description of what the tool does (used by the AI agent to decide when to use it).
    *   `args_schema`: Set this to your Pydantic input schema class (e.g., `args_schema: type[BaseModel] = MyToolInput`). If your tool takes no input, you might omit this or use a default.
8.  **Implement `_run` Method**: Define the `_run` method. This is the core logic of your tool. It receives the input parameters (defined in your `args_schema`) as arguments and should return a string result.

    ```python
    from gllm_agents import BaseTool
    from gllm_plugin.tools import tool_plugin
    from typing import Any # Import Any

    # ... (Assuming MyToolInput is defined as above)

    @tool_plugin(version="1.0.0")
    class MyCustomTool(BaseTool):
        name: str = "my_custom_tool"
        description: str = "Describes what my custom tool does."
        args_schema: type[BaseModel] = MyToolInput

        def _run(self, parameter1: str, parameter2: int, **kwargs: Any) -> str:
            # --- Your tool's logic goes here ---
            result = f"Processed {parameter1} and {parameter2}"
            # --- End of logic ---
            return result # Return a string
    ```
    
9.  **Upload and Use**: Once created, you can upload this new tool `.py` file to GLChat using the steps in the [Upload tool to GLChat](#upload-tool-to-glchat) section and configure an agent to use it.
