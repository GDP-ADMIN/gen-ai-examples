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
   
3. Navigate to the `custom-tool-and-agent` directory
4. Install all dependencies specified in the lock file

   ```bash
   poetry install
   ```

## Tool Development Guide

### Creating Basic Tools with the Decorator
1. Open your VSCode
2. Activate the newly installed virtual environment. VSCode usually activates this environment automatically. If it doesn't activate the environment automatically, then you should click it and select the python from this path `/custom-tool-and-agent/.venv/bin/python`.

   <img width="203" alt="image" src="https://github.com/user-attachments/assets/3dffba0d-8cd7-4577-880b-ea74d0080b7c" />

3. Create a new Python (`.py`) file and name it to `weather_forecast_tool.py`
4. The simplest way to create a new tool is using the `@tool_plugin` decorator:

    ```python
   from typing import Any
   from langchain_core.tools import BaseTool
   from pydantic import BaseModel, Field
   from gllm_plugin.tools import tool_plugin
   
   # Input schema definition
   class WeatherForecastInput(BaseModel):
       """Input schema for the weather forecast tool."""
       day: str = Field(..., description="Day of the week for the weather forecast (e.g., 'Monday')")
   
   # Tool implementation with decorator
   @tool_plugin(version="1.0.0")
   class WeatherForecastTool(BaseTool):
       """A tool to get weather forecast for a specific day for all supported locations."""
   
       name: str = "weather_forecast_tool"
       description: str = "Gets weather forecast for a specified day for all supported locations."
       args_schema: type[BaseModel] = WeatherForecastInput
   
       # Mock weather data
       _weather_data = {
           "New York": {
               "Monday": {"condition": "Sunny", "temperature": 25, "humidity": 60},
               "Tuesday": {"condition": "Partly Cloudy", "temperature": 23, "humidity": 65},
               "Wednesday": {"condition": "Cloudy", "temperature": 22, "humidity": 70},
               "Thursday": {"condition": "Rainy", "temperature": 20, "humidity": 80},
               "Friday": {"condition": "Thunderstorm", "temperature": 19, "humidity": 85},
               "Saturday": {"condition": "Cloudy", "temperature": 21, "humidity": 75},
               "Sunday": {"condition": "Sunny", "temperature": 24, "humidity": 65}
           },
           "London": {
               "Monday": {"condition": "Rainy", "temperature": 18, "humidity": 75},
               "Tuesday": {"condition": "Cloudy", "temperature": 17, "humidity": 70},
               "Wednesday": {"condition": "Partly Cloudy", "temperature": 19, "humidity": 65},
               "Thursday": {"condition": "Sunny", "temperature": 21, "humidity": 60},
               "Friday": {"condition": "Partly Cloudy", "temperature": 20, "humidity": 65},
               "Saturday": {"condition": "Cloudy", "temperature": 18, "humidity": 70},
               "Sunday": {"condition": "Rainy", "temperature": 17, "humidity": 75}
           },
           "Tokyo": {
               "Monday": {"condition": "Sunny", "temperature": 28, "humidity": 55},
               "Tuesday": {"condition": "Sunny", "temperature": 29, "humidity": 50},
               "Wednesday": {"condition": "Partly Cloudy", "temperature": 27, "humidity": 60},
               "Thursday": {"condition": "Cloudy", "temperature": 26, "humidity": 65},
               "Friday": {"condition": "Rainy", "temperature": 24, "humidity": 75},
               "Saturday": {"condition": "Thunderstorm", "temperature": 23, "humidity": 80},
               "Sunday": {"condition": "Cloudy", "temperature": 25, "humidity": 70}
           }
       }
   
       # Core method for any tool which implements the tool's functionality
       def _run(self, day: str, **kwargs: Any) -> str:
           """Run the weather forecast tool for a specific day for all locations."""
           try:
               day = day.capitalize()
               locations = list(self._weather_data.keys())
               forecast = f"Weather forecast for {day}:\n\n"
               for location in locations:
                   day_data = self._weather_data[location].get(day)
                   if not day_data:
                       forecast += f"{location}: No data available.\n"
                       continue
                   temp = day_data["temperature"]
                   forecast += f"{location}: {day_data['condition']}, {temp}°C, Humidity: {day_data['humidity']}%\n"
               return forecast
           except Exception as e:
               return f"Error providing weather forecast: {e}"
    ```
    
   Copy the above code in your newly created Python file
5. Check the import statements, ensure that there's no import error

### Upload tool to GL Chat
1. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in Gloria
2. Select the "Tools" menu and click the "Upload Tool" button
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/90d0b2fa-b481-4f56-a90e-c2f0c0340f41" />

3. Upload your newly created tool
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/7c39ec3a-7760-476d-a105-133322c1e823" />

4. Upon successful upload, your tool should appear in the "Custom Tools" menu
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/f7c575e2-907b-4138-9b30-549b0dde0a6d" />

## Agent Development Guide

### Creating a Single Agent

Let's create an agent with the ability to make weather forecast. We will be using the weather forecast tool we created in previous steps. You can also use the [weather_forecast_tool.py](/sample_tools/weather_forecast_tool.py) in the [sample_tools](/sample_tools) folder.

#### Here's the general workflow for creating an agent in Gloria:
1. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in Gloria
2. Select the "Tools" menu and click the "Upload Tool" button
3. Upload the `weather_forecast_tool.py` file
4. Upon successful upload, the `weather_forecast_tool` should appear in the "Custom Tools" menu
5. Select the "Agent" menu and click the "Create Agent" button
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/a40d6af6-9731-4547-8610-2e729df03483" />

6. Fill in all the required fields, for example:
   
    <img width="960" alt="image" src="https://github.com/user-attachments/assets/06979d3a-e173-4872-8ad4-6c216dae0f7b" />

   - **Agent Name**: weather_forecast_agent
   - **Agent Display Name**: Weather Forecast Agent
   - **Description**: This is a weather forecast agent
   - **Model**: gpt-4o
   - **Tools**: `weather_forecast_agent`
   - **Sub-Agents**: -
   - **Timeout**: 60
   - **Instructions**:
   ```
   You are an agent that can make a weather forecast prediction.

   You are provided with tools to help you make a weather forecast.
   Always use the provided tools when make a weather forecast, do not assume or make up your own answer.
   ```
   **Note**: Since we are creating a single agent, leave the Sub-Agents field empty.

7. Click the "Save" button
8. Upon successful creation, the Timer Agent should appear in the "Custom Agents" menu

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/cb908db2-902c-43d9-993c-e5b25c02eba3" />

### Testing - Converse with Agent

Since we can't yet deploy the newly created agent directly to Gloria, we provide a template agent that you can edit according to your custom agent, in this case the Weather Forecast Agent. The template agent is named Hello World Agent.

1. Open the [Agent Setting](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/agent-setting/agent) menu in Gloria
2. Select "Custom Agent"
3. Select triple dots icon on the Hello World Agent card and then click "Edit"

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/76e52736-af51-4c98-8493-ba0a0a21836d" />
   
4. Fill in all fields according to our newly created Weather Forecast Agent, except for the **Agent Name** field

   <img width="960" alt="image" src="https://github.com/user-attachments/assets/99460f62-c420-4d58-b09f-57ad5c2c20e4" />

5. Click "Save"
6. Open the [Chatbot menu](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/?chatbot_id=general-purpose) page in Gloria
7. In the Chatbot Selection, select "Demo General Purpose"

   <img width="443" alt="image" src="https://github.com/user-attachments/assets/053a5ca4-d387-4595-a14e-46c04c440ef6" />

8. Select the "More Agents" and scroll down, you should see the "Weather Forecast Agent"

   <img width="509" alt="image" src="https://github.com/user-attachments/assets/95382787-0def-4a40-bae3-ff0623d0107f" />

9. Ask a question to the Weather Forecast Agent

   <img width="679" alt="image" src="https://github.com/user-attachments/assets/b68a5e41-5390-4670-b480-6be8b4253181" />

