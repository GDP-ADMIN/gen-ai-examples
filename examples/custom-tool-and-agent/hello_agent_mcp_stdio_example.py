import asyncio
import dotenv

from gllm_agents import Agent
from gllm_agents.mcp.client import MCPClient
from langchain_openai import ChatOpenAI
from mcp_configs.configs import mcp_config_stdio

dotenv.load_dotenv()

async def main():
    async with MCPClient(mcp_config_stdio) as client:
        tools = client.get_tools()

        print("\033[1mAvailable tools:\033[0m")
        print(str([tool.name for tool in tools]))
        
        llm = ChatOpenAI(model="gpt-4.1")
        agent = Agent(
            name="HelloAgent",
            instruction="You are a helpful assistant that can calculate math problems using the provided tools.",
            llm=llm,
            tools=tools,
            verbose=True
        )

        query = "What is the square root of ((2 + 3 * 2) ^ 2)?"
        print(f"\033[1mRunning agent with prompt\033[0m: {query}")
        response = await agent.arun(query)
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
