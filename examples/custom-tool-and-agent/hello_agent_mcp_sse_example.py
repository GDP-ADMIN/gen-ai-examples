import asyncio
import dotenv

from gllm_agents import Agent
from langchain_openai import ChatOpenAI
from mcp_client import MCPClient
from mcp_configs.configs import mcp_config_sse

dotenv.load_dotenv()

async def main():
    async with MCPClient(mcp_config_sse) as client:
        tools = client.get_tools()

        print("Available tools:")
        print(str([tool.name for tool in tools]))
        
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

if __name__ == "__main__":
    asyncio.run(main())
