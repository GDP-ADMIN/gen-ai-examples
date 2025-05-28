"""Tool to search Google Serper API.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
    Fachriza Adhiatma (fachriza.d.adhiatma@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from datetime import datetime, timezone
import logging
from json import dumps
from typing import Type

from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

FORMAT_STRING = "%m/%d/%y %H:%M:%S"


class GoogleSerperInput(BaseModel):
    """Input schema for the GoogleSerperTool."""

    query: str = Field(..., description="Search query")


class GoogleSerperTool(BaseTool):
    """Tool to search Google Serper API."""

    name: str = "google_serper"
    description: str = """
    Useful for searching the web using the Google Serper API.
    Input should be a search query.
    """
    save_output_history: bool = Field(default=True)
    args_schema: Type[BaseModel] = GoogleSerperInput
    api_wrapper: GoogleSerperAPIWrapper

    def _run(
        self,
        query: str,
    ) -> str:
        """Executes a query using the API wrapper and returns the result as a JSON string.

        Args:
            query (str): The query string to be executed.
            run_manager (Optional[CallbackManagerForToolRun], optional): An optional callback manager for the tool run.
                Defaults to None.

        Returns:
            str: The result of the query execution, serialized as a JSON string.
        """
        result = self.api_wrapper.results(query)
        return dumps(result)


class TimeTool(BaseTool):
    """Tool to get the current time."""

    name: str = "time_tool"
    description: str = "Useful for getting the current time."

    def _run(self) -> str:
        return datetime.now(timezone.utc).strftime(FORMAT_STRING)
