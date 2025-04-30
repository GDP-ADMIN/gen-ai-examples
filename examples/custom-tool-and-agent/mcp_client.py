from langchain_mcp_adapters.client import MultiServerMCPClient

class MCPClient:
    def __init__(self, connections: list[dict]):
        self.connections = connections
        self.client = None
        self._initialized = False
        
    async def initialize(self):
        if self._initialized:
            return
            
        self.client = MultiServerMCPClient()
        
        # Connect to each server one at a time
        for server_name, connection in self.connections.items():
            await self.client.connect_to_server(server_name, **connection)
            
        self._initialized = True
        
    def get_tools(self):
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call 'await client.initialize()' first.")
        return self.client.get_tools()
        
    async def cleanup(self):
        if self.client and self._initialized:
            await self.client.exit_stack.aclose()
            self._initialized = False
