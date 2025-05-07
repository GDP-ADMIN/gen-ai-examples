from abc import ABC, abstractmethod
from typing import Any

from gllm_agents import BaseTool
from langchain_core.tools import StructuredTool, ToolException
from mcp import ClientSession, StdioServerParameters, stdio_client

import logging
import asyncio

from mcp.client.sse import sse_client
from mcp.types import CallToolResult, ImageContent, EmbeddedResource, TextContent

from client.tool import MCPTool

NonTextContent = ImageContent | EmbeddedResource


def _convert_call_tool_result(
    call_tool_result: CallToolResult,
) -> tuple[str | list[str], list[NonTextContent] | None]:
    text_contents: list[TextContent] = []
    non_text_contents = []
    for content in call_tool_result.content:
        if isinstance(content, TextContent):
            text_contents.append(content)
        else:
            non_text_contents.append(content)

    tool_content: str | list[str] = [content.text for content in text_contents]
    if not text_contents:
        tool_content = ""
    elif len(text_contents) == 1:
        tool_content = tool_content[0]

    if call_tool_result.isError:
        raise ToolException(tool_content)

    return tool_content, non_text_contents or None


class MCPConnection(ABC):
    transport: str
    inputs: dict[str, Any]
    tools: dict[str, BaseTool]
    
    _session_context: ClientSession | None = None
    _session: ClientSession | None = None
    _streams: Any = None
    _streams_context: Any = None

    def __init__(
        self,
        transport: str,
        inputs: dict[str, Any],
        log_level: int = logging.INFO,
        timeout: float = 10.0
    ):
        self.transport = transport
        self.inputs = inputs
        self.log_level = log_level
        self.timeout = timeout
        self._session = None
        self._session_context = None
        self._streams_context = None
        self.logger = logging.getLogger(f"mcp_{transport}")

    async def get_tools(self) -> dict[str, MCPTool]:
        print("Getting tools from session")
        tools = await self._session.list_tools()

        tools_map = {}
        for tool in tools.tools:
            print(f"Adding tool to map: {tool.name}")
            tools_map[tool.name] = MCPTool(self._session, tool)

        return tools_map

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "MCPConnection":
        if d["transport"] == "stdio":
            return StdioConnection(d["command"], d.get("args", []), d.get("inputs", {}))
        elif d["transport"] == "sse":
            return SseConnection(d["url"], d.get("inputs", {}))
        elif d["transport"] == "stream":
            return HttpStreamConnection(d["url"], d.get("inputs", {}))
        else:
            raise ValueError(f"Unknown transport: {d['transport']}")
        
    async def connect(self):
        await self._internal_connect()
        try:
            print("Connecting to streams")
            # Add timeout to prevent indefinite waiting
            try:
                self._streams = await asyncio.wait_for(
                    self._streams_context.__aenter__(), 
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                # kill process
                self._streams_context.__aexit__(None, None, None)
                # cancel asyncio
                asyncio.current_task().cancel()
                raise TimeoutError(f"Connection timed out after {self.timeout} seconds")
                
            print("Creating session")
            self._session_context = ClientSession(*self._streams)
            print("Entering session")
            self._session = await self._session_context.__aenter__()

            print("Initializing session")
            await self._session.initialize()
        except Exception as e:
            # Clean up resources if an error occurs during connection
            if self._session_context:
                await self._session_context.__aexit__(type(e), e, None)
            if self._streams_context:
                await self._streams_context.__aexit__(type(e), e, None)
            raise RuntimeError(f"Connection failed: {str(e)}") from e

    @abstractmethod
    async def _internal_connect(self):
        pass

    async def disconnect(self):
        print("Disconnecting from session")
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        print("Disconnecting from streams")
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)

class StdioConnection(MCPConnection):
    command: str
    args: list[str]

    def __init__(self, command: str, args: list[str], inputs=None):
        super().__init__("stdio", inputs)
        if inputs is None:
            inputs = {}
        self.inputs = inputs
        self.command = command
        self.args = args

    async def _internal_connect(self):
        import os
        import shutil
        
        # Check if the command exists as a file or in PATH before continuing
        if not (os.path.isfile(self.command) or shutil.which(self.command)):
            raise FileNotFoundError(f"Command not found: {self.command}")
            
        parameters = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=self.inputs
        )
        self._streams_context = stdio_client(parameters)

class SseConnection(MCPConnection):
    url: str

    def __init__(self, url: str, inputs: dict[str, str] = {}):
        super().__init__("sse", inputs)
        self.url = url

    async def _internal_connect(self):
        import urllib.parse
        
        # Basic URL validation
        try:
            parsed = urllib.parse.urlparse(self.url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError(f"Invalid URL format: {self.url}")
        except Exception as e:
            raise ValueError(f"Invalid URL: {self.url}") from e
            
        self._streams_context = sse_client(url=self.url)

class HttpStreamConnection(MCPConnection):
    url: str

    def __init__(self, url: str, inputs: dict[str, str] = {}):
        super().__init__("stream", inputs)
        self.url = url

    async def _internal_connect(self):
        raise NotImplementedError("HTTP stream connection is currently not supported by Python's MCP SDK")
