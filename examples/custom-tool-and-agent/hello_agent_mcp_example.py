import asyncio
import dotenv

from gllm_agents import Agent
from langchain_mcp_adapters.client import (MultiServerMCPClient, SSEConnection,
                                           StdioConnection,
                                           WebsocketConnection)
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class MCPClient:
    def __init__(self, connections: list[StdioConnection | SSEConnection | WebsocketConnection]):
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


async def main():
    client = MCPClient(
        {
            "hello": {
                "command": "python",
                "args": ["mcp_tools/hello_tool_stdio.py"],
                "transport": "stdio",
            },
            "goodbye": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )

    await client.initialize()
    
    try:
        llm = ChatOpenAI(model="gpt-4o")
        agent = Agent(
            name="HelloAgent",
            instruction="You are a helpful assistant that can greet people by name using the provided tool.",
            llm=llm,
            tools=client.get_tools(),
            verbose=True
        )
        hello_response = await agent.arun("Say hello to World")
        goodbye_response = await agent.arun("Say goodbye to World")
        no_tool_response = await agent.arun("What's going on?")

        print(hello_response)
        print(goodbye_response)
        print(no_tool_response)
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
