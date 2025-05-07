# bosa_twitter_tool.py
import os
from bosa_connectors.connector import BosaConnector
from gllm_agents import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Type
from dotenv import load_dotenv

load_dotenv()

# Optional: Define input schema if the tool needs arguments
class TwitterUserInput(BaseModel):
    username: str = Field(..., description="The username of target user to search for.")

class BosaTwitterGetUserTool(BaseTool):
    """A tool to search twitter user using BOSA by input username."""
    name: str = "bosa_twitter_tool"
    description: str = "Search twitter user using BOSA by input username."
    args_schema: Type[BaseModel] = TwitterUserInput

    def _run(self, username: str,  **kwargs: Any) -> str:
        """Uses the tool."""
        api_base_url = os.getenv("BOSA_API_BASE_URL", "https://staging-api.bosa.id")
        api_key = os.getenv("BOSA_API_KEY", "")
        bosa_connector = BosaConnector(api_base_url=api_base_url, api_key=api_key)

        params = {
            "username": username,
        }
        
        try:
            result = bosa_connector.execute("twitter", "get-users", max_attempts=1, input_=params)
        except Exception as e:
            result = f"An error occurred: {str(e)}. Please try again."
        return result
