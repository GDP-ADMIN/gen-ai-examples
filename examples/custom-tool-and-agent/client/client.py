from .connection import MCPConnection
from .tool import MCPTool

class MCPClient:

    connections: dict[str, MCPConnection]

    failed_connections: dict[str, str]

    def __init__(self, connection: dict[str, dict | MCPConnection]):
        self.connections = {}
        for key, value in connection.items():
            if isinstance(value, dict):
                self.connections[key] = MCPConnection.from_dict(value)
            else:
                self.connections[key] = value

    async def get_tools(self) -> dict[str, MCPTool]:
        tools = {}
        for connection in self.connections.values():
            print("Getting tools from connection")
            tools.update(await connection.get_tools())
        return tools

    async def __aenter__(self):
        try:
            for key, connection in self.connections.items():
                await connection.connect()
        except Exception as e:
            print(f"Error connecting to connections: {e}")
            self.failed_connections[key] = str(e)
            raise e
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            for key, connection in self.connections.items():
                if key in self.failed_connections:
                    continue
                await connection.disconnect()
        except Exception as e:
            print(f"Error disconnecting from connections: {e}")
        return self
