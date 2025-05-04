"""MCP Client Module for GLLM Agents.

This module defines the MCPClient class which serves as a client for connecting to MCP servers.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)

References:
    - https://modelcontextprotocol.io/introduction
    - https://github.com/langchain-ai/langchain-mcp-adapters
"""

import logging
from types import TracebackType
from typing import Optional, Type

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient


class MCPClient:
    """MCP Client for GLLM Agents.

    This class provides a client for connecting to MCP servers.

    Attributes:
        connections (dict[str, dict]): Dictionary of connection dictionaries for MCP servers.
        client (MultiServerMCPClient): The MCP client instance.
        failed_connections (dict[str, Exception]): Dictionary of failed connections.
    """

    def __init__(
        self,
        connections: dict[str, dict],
        log_level: int = logging.DEBUG,
    ):
        """Initialize the MCPClient with the provided connections.

        Example on how to initialize:
        ```python
        client = MCPClient({
            "sse": {
                "url": "http://localhost:8000",
                "transport": "sse",
            },
            "stdio": {
                "command": "python",
                "args": ["path/to/python/file.py"],
                "transport": "stdio",
            },
        })
        client = MCPClient(connections)
        async with client:
            tools = client.get_tools()
        ```

        Right now, as per the Langchain's MCP Adapter Library, the only supported transports
        are "sse" and "stdio". Python MCP also currently does not support HTTP Streams.

        Args:
            connections (dict[str, dict]): Dictionary of connection dictionaries for MCP servers.
        """
        self.connections = connections
        self.client: Optional[MultiServerMCPClient] = None
        # TODO: Implement tracking of failed connections as a future improvement
        self.failed_connections: dict[str, Exception] = {}
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    def get_tools(self) -> list[BaseTool]:
        """Get the tools from the MCPClient.

        This method returns the tools from the MCPClient. Example:

        ```python
        tools = client.get_tools()
        ```
        """
        if self.client is None:
            self.logger.error("MCPClient is not initialized. Please use 'async with' to initialize it.")
            raise RuntimeError("MCPClient is not initialized. Please use 'async with' to initialize it.")
        return self.client.get_tools()

    async def __aenter__(self):
        """Initialize the MCPClient and connect to servers.

        Called automatically when entering an `async with` block.

        Returns:
            MCPClient: The initialized client instance.

        Raises:
            RuntimeError: If unable to initialize the core MCP client or
                          if all server connections fail.
        """
        if self.client is not None:
            self.logger.debug("MCPClient __aenter__ called but client was already initialized.")
            return self

        try:
            self.logger.info("Initializing MultiServerMCPClient...")
            self.client = MultiServerMCPClient()
        except Exception as e:
            self.logger.error(f"Failed to initialize MultiServerMCPClient: {e}", exc_info=True)
            raise RuntimeError("Failed to initialize core MCP client") from e

        # TODO: Implement more robust error handling for connection failures
        for server_name, connection in self.connections.items():
            self.logger.info(f"Attempting to connect to MCP server '{server_name}'...")
            try:
                await self.client.connect_to_server(server_name, **connection)
                self.logger.info(f"Successfully connected to MCP server '{server_name}'...")
            except Exception as e:
                self.logger.error(f"Failed to connect to MCP server '{server_name}': {e}", exc_info=True)
                # TODO: Handle connection failure and add to failed_connections

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Clean up the MCPClient connections.

        Called automatically when exiting an `async with` block.

        Args:
            exc_type: The type of exception that was raised.
            exc_val: The exception that was raised.
            exc_tb: The traceback of the exception.

        Returns:
            None
        """
        if self.client:
            self.logger.info("Cleaning up MCP client connections...")
            try:
                await self.client.exit_stack.aclose()
                self.logger.info("MCP client connections cleaned up successfully.")
            except Exception as e:
                self.logger.error(f"Error during MCP client cleanup: {e}", exc_info=True)
            finally:
                self.client = None
        else:
            self.logger.debug("MCPClient __aexit__ called but client was not initialized.")
