from gllm_agents import BaseTool
from mcp import ClientSession
from mcp.types import Tool
from pydantic import create_model, Field
from typing import Any, Dict, Optional, Type

def json_schema_to_pydantic(schema: Dict[str, Any]) -> Type:
    """Convert a JSON schema to a Pydantic model."""
    if not schema or not isinstance(schema, dict):
        return None
    
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    fields = {}
    
    for name, prop in properties.items():
        field_type = Any  # Default to Any
        if prop.get("type") == "integer":
            field_type = int
        elif prop.get("type") == "number":
            field_type = float
        elif prop.get("type") == "string":
            field_type = str
        elif prop.get("type") == "boolean":
            field_type = bool
            
        # Make field optional if not in required list
        if name in required:
            fields[name] = (field_type, ...)
        else:
            fields[name] = (Optional[field_type], None)
    
    return create_model(schema.get("title", "ArgumentModel"), **fields)

class MCPTool(BaseTool):
    session: ClientSession = None
    tool: Tool = None
    
    def __init__(
        self,
        session: ClientSession,
        tool: Tool
    ):
        # Convert JSON schema to Pydantic model
        args_schema = json_schema_to_pydantic(tool.inputSchema)
        print(f"Args schema: {args_schema.model_json_schema()}")
        super().__init__(
            name=tool.name,
            description=tool.description,
            args_schema=args_schema,
        )
        self.session = session
        self.tool = tool

    def _run(self, **kwargs: Any) -> Any:
        raise NotImplementedError(f"Tool {self.name} does not support sync execution.")

    async def _arun(self, **kwargs: Any) -> Any:
        print(f"Calling tool: {self.tool.name} with kwargs: {kwargs}")
        result = await self.session.call_tool(self.tool.name, kwargs)
        print(f"Tool result: {result}")
        return result
