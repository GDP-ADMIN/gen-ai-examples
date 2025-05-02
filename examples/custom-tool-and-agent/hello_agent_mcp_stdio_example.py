import asyncio
import dotenv

from gllm_agents import Agent
from langchain_openai import ChatOpenAI
from mcp_client import MCPClient
from mcp_configs.configs import mcp_config_stdio

dotenv.load_dotenv()

async def main():
    client = MCPClient(mcp_config_stdio)

    await client.initialize()
    tools = client.get_tools()

    print("Available tools:")
    print(str([tool.name for tool in tools]))
    
    try:
        llm = ChatOpenAI(model="gpt-4.1")
        agent = Agent(
            name="HelloAgent",
            instruction="You are a helpful assistant that can greet people by name using the provided tool.",
            llm=llm,
            tools=tools,
            verbose=True
        )

        response = await agent.arun("What is the square root of ((2 + 3 * 2) ^ 2)?")
        print(response)

    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
