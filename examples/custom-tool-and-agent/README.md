# Custom Tool and Agent Hello World
This is an example how to create custom tool and agent.

## Prerequisites

> [!NOTE]
> You need to fulfill the prerequisites to run the script.

1. **Python v3.12** (to run `python`)

   - Using Conda (recommended):

     You can use [Miniconda](https://docs.anaconda.com/miniconda/install) to install and manage Python versions.

   - <details>
     <summary>Using Python installer (alternative)</summary>
     
     You can download the Python installer from the link [Python 3.12.8](https://www.python.org/downloads/release/python-3128/), select the version appropriate for your operating system, and run the installer.

     > [!NOTE]
     > For Windows, please make sure to check the `Add python.exe to PATH` option during the installation process.
   </details>

2. **Google Cloud CLI v493.0.0 or above** (to run `gcloud`).

   - You can install it by following [this instruction](https://cloud.google.com/sdk/docs/install).
   - After installing it, sign in to your account using `gcloud auth login` command.
   - If the `gcloud` CLI asks you to enter project ID, enter `gdp-labs`.

3. **Access to GDP-ADMIN/gen-ai-internal repository**

   You can try to access the [GDP-ADMIN/gen-ai-external](https://github.com/GDP-ADMIN/gen-ai-external) repository in your browser. If you don’t have access, please make a request to ticket(at)gdplabs.id.

4. **SSH Key in your GitHub Account**

   You must add your SSH key to your GitHub account. Please follow this instruction by GitHub: [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account). This is required as this sample has dependency to a private GitHub repository.

5. **Access to the GDP Labs Google Artifact Registry**.
   - This is required for `poetry` to download necessary dependencies.
   - If you don't have access, please make a request to ticket(at)gdplabs.id.

   **Notes**:\
   If you're unsure whether you already have access, simply proceed to the next step. The script in step 4 of the [Installing Dependencies](#installing-dependencies) section will automatically check your access status. If you don't have the necessary permissions, you'll see this error message: `User does not have access to the GDP Labs Google Artifact Registry. Please contact the GDP Labs DSO team at infra(at)gdplabs.id.`

7. **VSCode IDE**
   - Go to [VSCode](https://code.visualstudio.com/download) to download VSCode IDE.

## Installing Dependencies

1. Open a terminal (on Mac/Linux) or command prompt (on Windows)

2. Clone the `gen-ai-examples` repository.

   ```bash
   git clone https://github.com/GDP-ADMIN/gen-ai-examples.git
   ```

3. Navigate to the example directory:

   ```bash
   cd gen-ai-examples/examples/custom-tool-and-agent
   ```

4. Execute the script:

   - For Linux, macOS, or Windows WSL:

     ```bash
     ./local-start.sh
     ```

   - <details>
     <summary>For Windows (alternative)</summary>

     > [!NOTE]
     > On Windows, you can either install [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install) and use the command above, or execute the batch file directly in Windows Powershell or Command Prompt as shown below.

     - For Windows Powershell:

       ```powershell
       .\local-start.bat
       ```

     - For Windows Command Prompt:

       ```cmd
       local-start.bat
       ```
     </details>

## Setting Python Interpreter Path in VSCode IDE

Set up the Python interpreter path in your IDE by following these instructions:

> [!WARNING]
> You must complete the steps in [Installing Dependencies](#installing-dependencies) until you see the `custom-tool-and-agent example finished running.` on the console before continuing with the steps below on this section.

1. Open your VScode within the `gen-ai-examples/examples/custom-tool-and-agent` directory.
2. On the left side-bar, click the "Extensions" menu (Ctrl+Shift+X). Type "Python" in the Search Bar and then click an extension named "Python" from "Microsoft". Finally, click the "Install" button.

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/04d437fd-51b8-4b01-b28b-b585db091fce" />
   
4. Open the Python code sample [weather_forecast_tool.py](./sample_tools/weather_forecast_tool.py)

   Notice that there are either red or yellow squiggly underlines beneath `import` statements (like `from gllm_plugin.tools import tool_plugin`) in the VSCode editor.

   <img width="579" alt="image" src="https://github.com/user-attachments/assets/72979f2b-16b1-4265-8d30-dfab96cd6a61" />
   
5. After you run `./local-start.sh` using steps in [Installing Dependencies](#installing-dependencies), you will see the log `PYTHON_PATH will be set to:` in the console. Copy the path in the next line, which looks something like:
   ```
   /home/<username>/gen-ai-examples/examples/custom-tool-and-agent/.venv/bin/python3
   ```
6. Open command palette (`⌘+Shift+P` for Mac or `Ctrl+Shift+P` for Linux/Windows) and type `> Python: Select Interpreter` and press enter.

   <img width="493" alt="image" src="https://github.com/user-attachments/assets/2e463386-3424-45b0-8e2e-b9b7adab21b0" />
   
7. Select `Enter interpreter path...`
8. Paste the previously copied path from the console and press enter.

   <img width="501" alt="image" src="https://github.com/user-attachments/assets/3fc2db14-d8e5-45fd-9f74-e7f59cf84abc" />

9. Check the bottom status bar in VSCode (as shown in the image below) to ensure the selected Python interpreter points to the `.venv` environment created by Poetry (e.g., `Python 3.11.10 ('.venv')`).

   <img width="203" alt="image" src="https://github.com/user-attachments/assets/3dffba0d-8cd7-4577-880b-ea74d0080b7c" />

   Your IDE will then recognize the path and will no longer show red squiggly lines under the import statements. You can try hovering over them to see the details of the library.

   <img width="497" alt="image" src="https://github.com/user-attachments/assets/342841b3-0205-4b0b-869f-ea7d959ad1cd" />

## Tool Development Guide

### Creating a Custom Tool
1. Open your VSCode within the `gen-ai-examples/examples/custom-tool-and-agent` directory.
2. You can create your own tool following guide on the [Advanced: Developing Your Own Custom Tool](#advanced-developing-your-own-custom-tool) section. But, for simplicity, let's use sample tool [weather_forecast_tool.py](./sample_tools/weather_forecast_tool.py).
   *   The sample file demonstrates the basic structure of a tool using the `@tool_plugin` decorator.
   *   **What this tool does**: This sample tool provides weather forecasts for specific days of the week across multiple cities (New York, London, and Tokyo). It uses mock weather data stored within the tool itself and takes a day of the week as input. The tool returns formatted weather information including condition, temperature, and humidity for each location.
3. Open the `weather_forecast_tool.py` file in VSCode.
5. Check the import statements. Ensure that there are no import errors.
   *   **What are import errors?** These errors mean that Python cannot find a specific piece of code (a library or module) that the tool needs to function. This usually happens if a required dependency wasn't installed correctly or if VSCode isn't using the correct Python environment where the dependencies were installed.
   *   **How to check**: Look for any red squiggly underlines beneath `import` statements (like `from gllm_plugin.tools import tool_plugin`) in the VSCode editor. These visual cues indicate a problem. You can also open the "Problems" panel in VSCode (usually accessible via the View menu or by clicking the error/warning icons in the bottom status bar) to see a list of specific errors.
   *   If you see import errors, double-check that you have activated the correct virtual environment (Step 2 - verify the Python interpreter in the status bar) and the script `local-start` (Step 4 under [Installing Dependencies](#installing-dependencies)) completed without errors.
   *   Once you've successfully run through this example, see the [Advanced: Developing Your Own Custom Tool](#advanced-developing-your-own-custom-tool) section at the end of this document for guidance on creating tools beyond this sample.

### Upload tool to GLChat
1. Open your browser and navigate to the [GLChat login page](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/).
2. Log in using your credentials (e.g., Sign in with Google).

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/13f114ac-1f22-4195-8294-37d498d669fe" />

4. After logging in, click on the "Admin Dashboard" button.

    <img width="960" alt="image" src="https://github.com/user-attachments/assets/29217848-33a4-4010-8d21-43cb6c4f7258" />

5. In the Admin Dashboard, locate the "AI Agent" section in the left sidebar and click on "Tools". The **staging** URL should be [https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin/ai-agent/tools](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin/ai-agent/tools).

    <img width="240" alt="image" src="https://github.com/user-attachments/assets/fd451432-1766-4c19-af51-de78c3b0ef01" />

6. Click the "Upload Tool" button.

    <img width="960" alt="image" src="https://github.com/user-attachments/assets/2221f498-9d6a-40fb-b298-e2f26147a57f" />

7. Upload the `weather_forecast_tool.py` file you created/copied.

    <img width="960" alt="image" src="https://github.com/user-attachments/assets/7c39ec3a-7760-476d-a105-133322c1e823" />

4. Upon successful upload, your tool should appear in the "Custom Tools" menu
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/2f4ec7e3-0b82-4748-a492-49c8ecbbf5c7" />

### Testing and Validating the Tool

*This section is a work in progress. Steps for specifically testing and validating an uploaded tool before associating it with an agent will be added in a future update.*

## Agent Development Guide

### Creating a Single Agent

Let's create an agent with the ability to make weather forecast. We will be using the weather forecast tool we created in previous steps. You can also use the [weather_forecast_tool.py](/sample_tools/weather_forecast_tool.py) in the [sample_tools](/sample_tools) folder.

#### Here's the general workflow for creating an agent in GLChat:
1. Ensure the `weather_forecast_tool.py` tool has been uploaded to GLChat **staging** by following the steps in the "Upload tool to GLChat" section.
2. Ensure you are logged into the GLChat **staging** Admin Dashboard.
3. From the Admin Dashboard, navigate to the "AI Agent" section in the left sidebar and click on "Agent". The **staging** URL should be [https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin/ai-agent/agent](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin/ai-agent/agent).

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/3db6de93-eca1-4313-8deb-14cc1571a5fd" />

4. Click the "Create Agent" button.
6. Fill in all the required fields exactly as follows:

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

8. Click the "Save" button
9. Upon successful creation, the Weather Forecast Agent should appear in the "Custom Agents" menu

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/17507b12-a25c-4b6e-9758-faceded4184c" />

## Testing the Agent

Since direct deployment/assignment of newly created custom agents to chatbots in GLChat **staging** is not yet available (pending the Admin Dashboard feature), we provide a workaround using a pre-existing dummy agent named "Hello World Agent" that is already assigned to the "Demo General Purpose" chatbot in the **staging** environment. We will edit this existing agent to use our custom tool and instructions.

### Configure the Test Agent

1. Navigate back to the GLChat **staging** Admin Dashboard (ensure you are still logged in).
2. In the Admin Dashboard, locate the "AI Agent" section in the left sidebar and click on "Agent".
3. Select the "Agent" tab (it might be selected by default) and ensure "Custom Agent" is selected in the filter/dropdown.
4. Find the "Hello World Agent" card, click the triple dots icon (...), and then click "Edit".

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/c3d1b895-dd1b-47d2-b135-b1f4d47ff662" />

5. Fill in all fields according to the Weather Forecast Agent you defined previously (**except** for the **Agent Name** field).
   *   **Notes**: The field `Agent Name` is non-editable and it must remain `hello_world_agent` because this specific name is pre-assigned to the "Demo General Purpose" chatbot for testing purposes.
   *   Update the `Agent Display Name`, `Description`, `Model`, `Tools` (select `weather_forecast_tool`), `Timeout`, and `Instructions` to match your Weather Forecast Agent created previously in the [Creating a Single Agent](#creating-a-single-agent).

         <img width="960" alt="image" src="https://github.com/user-attachments/assets/4e294958-7024-48d9-8ad2-b4a87afadad1" />

6. Click "Save".

### Converse with Agent

1. Open the [GLChat **staging** Chat UI](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/) in your browser.

   **Tips:**
   If you are on the [Admin Dashboard](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin/knowledge-base) page, you can easily switch to the GLoria Chatbot UI by clicking your profile section at the bottom left of the page and selecting "Switch to GLoria Chatbot".

   <img width="191" alt="image" src="https://github.com/user-attachments/assets/5a4c5e2c-55f6-4269-9e11-b03f3734a3a5" />
   
3. From the left-hand sidebar, click on the "Chatbot" selection menu (it might initially say "Demo General Purpose").
4. Select "Demo General Purpose" from the dropdown list (this chatbot exists in the **staging** environment).

   <img width="443" alt="image" src="https://github.com/user-attachments/assets/053a5ca4-d387-4595-a14e-46c04c440ef6" />

5. In the chat interface, click the "More Agents" button. Scroll down, and you should see the "Weather Forecast Agent" (which is actually the edited "Hello World Agent" with your settings).

    <img width="509" alt="image" src="https://github.com/user-attachments/assets/95382787-0def-4a40-bae3-ff0623d0107f" />

6. Select the "Weather Forecast Agent" and ask it a question, like "What is the weather forecast for Tuesday?".

    <img width="679" alt="image" src="https://github.com/user-attachments/assets/b68a5e41-5390-4670-b480-6be8b4253181" />

### Cleanup The Agent

After you successfully test the Weather Forecast Agent, it's better to clean up your work so that others can test it with a clean state.

#### Reset Hello World Agent

1.   Navigate back to the GLChat **staging** Admin Dashboard.
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

1.   Navigate back to the GLChat **staging** Admin Dashboard.
2.   In the Admin Dashboard, locate the "AI Agent" section in the left sidebar and click on "Agent".
3.   Find the agent named "Weather Forecast Agent", click the triple dots icon, and then click "Delete".
4.   Make sure the agent is deleted in the UI.

#### Delete the `weather_forecast_tool`

1.   Navigate back to the GLChat **staging** Admin Dashboard.
2.   In the Admin Dashboard, locate the "AI Agent\" section in the left sidebar and click on \"Tools\".
3.   Select the \"Custom Tools\" section.
4.   Navigate to the `weather_forecast_tool`, click the triple dots, and then click "Delete".

      <img width="957" alt="image" src="https://github.com/user-attachments/assets/92c8cb42-5192-427f-84bb-bba05a296e96" />
5.   Make sure the tool is deleted in the UI.

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
    
9.  **Upload and Use**: Once created, you can upload this new tool `.py` file to GLChat **staging** using the steps in the [Upload tool to GLChat](#upload-tool-to-gl-chat) section and configure an agent to use it.
