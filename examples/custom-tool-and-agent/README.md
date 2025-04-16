# Custom Tool and Agent Hello World
This is an example how to create custom tool and agent.

## Pre-requisites

1. **Python v3.11 or above**:
   - Ensure that Python is installed and available in your environment. You can check using `python --version`.
     
      ```bash
      python --version
      ```

2. **[Poetry](https://python-poetry.org/docs/) v1.8.1 or above**:
   - Poetry is used for dependency management and packaging in Python projects. It simplifies the process of managing project dependencies and virtual environments. You can check using `poetry --version`.

      ```bash
      poetry --version
      ```

4. **[Google Cloud CLI](https://cloud.google.com/sdk/docs/install)**:
   - The `gcloud` CLI is required for authenticating to access private package repositories. Ensure it's installed and configured (`gcloud auth login`, `gcloud config set project <your-project-id>`).
   - Install the CLI by following the instructions at [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install).
   - After installation, configure it by running:
     
       ```bash
       gcloud auth login
       gcloud config set project <your-project-id>
       ```

5. **VSCode IDE**
   - Go to [VSCode](https://code.visualstudio.com/download) to download VSCode IDE.

6. **GDP Labs VPN**
   - The GDP Labs VPN is required to access the GLChat staging environment where tools are uploaded and agents are tested. Ensure you are connected to the VPN before proceeding with steps involving GLChat.

### Installing dependencies

1. Clone the `gen-ai-examples` repository.

   ```bash
   git clone https://github.com/GDP-ADMIN/gen-ai-examples.git
   ```

2. Navigate to the example directory:

   ```bash
   cd gen-ai-examples/examples/custom-tool-and-agent
   ```

3. Configure Poetry to authenticate with Google Artifact Registry (or other private repository):
   - This command uses your `gcloud` credentials to grant Poetry access to private packages required by the project.

      ```bash
      poetry config http-basic.gen-ai oauth2accesstoken "$(gcloud auth print-access-token)"
      ```

4. Install all dependencies specified in the lock file:

   ```bash
   poetry install
   ```

## Tool Development Guide

### Creating a Custom Tool
1. Open your VSCode within the `gen-ai-examples/examples/custom-tool-and-agent` directory.
2. Activate the newly installed virtual environment. VSCode usually activates this environment automatically. If it doesn't activate the environment automatically, then you should click it and select the python from this path `/custom-tool-and-agent/.venv/bin/python`.
   *   **Alternative**: You can also use the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`), type "Python: Select Interpreter", and choose the interpreter associated with the `.venv` directory within your project.
   *   **Verify**: Check the bottom status bar in VSCode (as shown in the image below) to ensure the selected Python interpreter points to the `.venv` environment created by Poetry (e.g., `Python 3.11.10 ('.venv')`).

         <img width="203" alt="image" src="https://github.com/user-attachments/assets/3dffba0d-8cd7-4577-880b-ea74d0080b7c" />

3. Create a new Python file named `weather_forecast_tool.py` in the current directory (`examples/custom-tool-and-agent`).
   *   Open a terminal. You can use the integrated terminal in VSCode (Terminal > New Terminal) or an external terminal window. Ensure your terminal's current working directory is `gen-ai-examples/examples/custom-tool-and-agent`.

         ```bash
        touch weather_forecast_tool.py
        ```
         
5. Open the newly created `weather_forecast_tool.py` file in VSCode.
6. Copy the entire content from the sample tool file located at `sample_tools/weather_forecast_tool.py` and paste it into your new `weather_forecast_tool.py`.
   *   The sample file demonstrates the basic structure of a tool using the `@tool_plugin` decorator.
7. Check the import statements. Ensure that there are no import errors.
   *   **What are import errors?** These errors mean that Python cannot find a specific piece of code (a library or module) that the tool needs to function. This usually happens if a required dependency wasn't installed correctly or if VSCode isn't using the correct Python environment where the dependencies were installed.
   *   **How to check**: Look for any red squiggly underlines beneath `import` statements (like `from gllm_plugin.tools import tool_plugin`) in the VSCode editor. These visual cues indicate a problem. You can also open the "Problems" panel in VSCode (usually accessible via the View menu or by clicking the error/warning icons in the bottom status bar) to see a list of specific errors.
   *   If you see import errors, double-check that you have activated the correct virtual environment (Step 2 - verify the Python interpreter in the status bar) and that `poetry install` (Step 4 under Installing Dependencies) completed without errors.
   *   Once you've successfully run through this example, see the [Advanced: Developing Your Own Custom Tool](#advanced-developing-your-own-custom-tool) section at the end of this document for guidance on creating tools beyond this sample.

### Upload tool to GL Chat
1. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in GLChat (ensure you are connected to the GDP Labs VPN).
2. Select the "Tools" menu and click the "Upload Tool" button
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/90d0b2fa-b481-4f56-a90e-c2f0c0340f41" />

3. Upload the `weather_forecast_tool.py` file you created/copied.

    <img width="960" alt="image" src="https://github.com/user-attachments/assets/7c39ec3a-7760-476d-a105-133322c1e823" />

4. Upon successful upload, your tool should appear in the "Custom Tools" menu
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/f7c575e2-907b-4138-9b30-549b0dde0a6d" />

### Testing and Validating the Tool

*This section is a work in progress. Steps for specifically testing and validating an uploaded tool before associating it with an agent will be added in a future update.*

## Agent Development Guide

### Creating a Single Agent

Let's create an agent with the ability to make weather forecast. We will be using the weather forecast tool we created in previous steps. You can also use the [weather_forecast_tool.py](/sample_tools/weather_forecast_tool.py) in the [sample_tools](/sample_tools) folder.

#### Here's the general workflow for creating an agent in GLChat:
1. Ensure the `weather_forecast_tool.py` tool has been uploaded to GLChat by following the steps in the "Upload tool to GL Chat" section.
2. Navigate back to the "Agent" menu and click the "Create Agent" button.
3. Fill in all the required fields, for example:

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/06979d3a-e173-4872-8ad4-6c216dae0f7b" />

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

4. Click the "Save" button
5. Upon successful creation, the Weather Forecast Agent should appear in the "Custom Agents" menu

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/cb908db2-902c-43d9-993c-e5b25c02eba3" />

## Testing the Agent

Since direct deployment/assignment of newly created custom agents to chatbots in GLChat is not yet available (pending the Admin Dashboard feature), we provide a workaround using a pre-existing dummy agent named "Hello World Agent" that is already assigned to the "Demo General Purpose" chatbot. We will edit this existing agent to use our custom tool and instructions.

### Converse with Agent

1. Open the [GLChat Chat UI](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/) in your browser (ensure you are connected to the GDP Labs VPN).
2. From the left-hand sidebar, click on the "Chatbot" selection menu (it might initially say "Demo General Purpose").
3. Select "Demo General Purpose" from the dropdown list.

   <img width="443" alt="image" src="https://github.com/user-attachments/assets/053a5ca4-d387-4595-a14e-46c04c440ef6" />

4. Go back to the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in GLChat.
5. Select the "Agent" tab and ensure "Custom Agent" is selected in the filter/dropdown.
6. Find the "Hello World Agent" card, click the triple dots icon (...), and then click "Edit".

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/76e52736-af51-4c98-8493-ba0a0a21836d" />

7. Fill in all fields according to the Weather Forecast Agent you defined previously (**except** for the **Agent Name** field).
   *   **Important**: Do **not** change the `Agent Name`. It must remain `Hello World Agent` because this specific name is pre-assigned to the "Demo General Purpose" chatbot for testing purposes.
   *   Update the `Agent Display Name`, `Description`, `Model`, `Tools` (select `weather_forecast_tool`), `Timeout`, and `Instructions` to match your Weather Forecast Agent.

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/99460f62-c420-4d58-b09f-57ad5c2c20e4" />

8. Click "Save".
9. Navigate back to the [Chatbot menu/page](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/?chatbot_id=general-purpose) in GLChat (where you selected "Demo General Purpose").
10. In the chat interface, click the "More Agents" button. Scroll down, and you should see the "Weather Forecast Agent" (which is actually the edited "Hello World Agent" with your settings).

    <img width="509" alt="image" src="https://github.com/user-attachments/assets/95382787-0def-4a40-bae3-ff0623d0107f" />

11. Select the "Weather Forecast Agent" and ask it a question, like "What is the weather forecast for Tuesday?".

    <img width="679" alt="image" src="https://github.com/user-attachments/assets/b68a5e41-5390-4670-b480-6be8b4253181" />

## Advanced: Developing Your Own Custom Tool

The steps above guide you through using the provided `weather_forecast_tool.py` sample. To create your *own* custom tool, follow these general principles (referencing concepts from the [Tool Implementation Document](tool_implementation.md) for more detail):

1.  **Create a Python File**: Create a new `.py` file for your tool (e.g., `my_calculator_tool.py`).
2.  **Import Necessary Modules**: You'll typically need `BaseTool` from `langchain_core.tools`, `BaseModel` and `Field` from `pydantic`, and the `tool_plugin` decorator from `gllm_plugin.tools`.
3.  **Define Input Schema (if needed)**: If your tool requires specific inputs, define a Pydantic `BaseModel` subclass. Use `Field` to add descriptions and validation for each input parameter.

    ```python
    from pydantic import BaseModel, Field

    class MyToolInput(BaseModel):
        parameter1: str = Field(..., description="Description for parameter 1")
        parameter2: int = Field(..., description="Description for parameter 2")
    ```
    
5.  **Create Tool Class**: Define a class that inherits from `langchain_core.tools.BaseTool`.
6.  **Add Decorator**: Apply the `@tool_plugin(version="...")` decorator to your class for automatic registration.
7.  **Set Class Attributes**: Define the required attributes within your class:
    *   `name`: A unique string identifier for your tool (e.g., `"my_calculator"`).
    *   `description`: A clear, concise description of what the tool does (used by the AI agent to decide when to use it).
    *   `args_schema`: Set this to your Pydantic input schema class (e.g., `args_schema: type[BaseModel] = MyToolInput`). If your tool takes no input, you might omit this or use a default.
8.  **Implement `_run` Method**: Define the `_run` method. This is the core logic of your tool. It receives the input parameters (defined in your `args_schema`) as arguments and should return a string result.

    ```python
    from langchain_core.tools import BaseTool
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
    
9.  **Upload and Use**: Once created, you can upload this new tool `.py` file to GLChat using the steps in the [Upload tool to GL Chat](#upload-tool-to-gl-chat) section and configure an agent to use it.
