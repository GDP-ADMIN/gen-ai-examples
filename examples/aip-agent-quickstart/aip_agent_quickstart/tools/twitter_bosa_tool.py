"""Defines a Twitter user tool that can be used to get the user details for a specified Twitter user.

Authors:
    Saul Sayers (saul.sayers@gdplabs.id)
"""

import logging
import os
import dotenv

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from bosa_connectors.connector import BosaConnector

logger = logging.getLogger(__name__)

dotenv.load_dotenv()


class TwitterUserInput(BaseModel):
    username: str = Field(..., description="The username of target user to search for.")


@tool(args_schema=TwitterUserInput)
def twitter_get_user_tool(username: str) -> str:
    """Retrieves details for specified Twitter user.

    Args:
        username: The username of target user to search for.

    Returns:
        A response of user details object from BOSA endpoint
    """
    api_base_url = os.getenv("BOSA_API_BASE_URL", "https://staging-api.bosa.id")
    api_key = os.getenv("BOSA_API_KEY", "")
    bosa_connector = BosaConnector(api_base_url=api_base_url, api_key=api_key)

    params = {
        "username": username,
    }

    try:
        result = bosa_connector.execute(
            "twitter", "get-users", max_attempts=1, input_=params
        )
    except Exception as e:
        result = f"An error occurred: {str(e)}. Please try again."
    return result
