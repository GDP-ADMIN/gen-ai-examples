import asyncio
import dotenv

from gllm_agents import Agent
from client.client import MCPClient
from langchain_openai import ChatOpenAI
from mcp_configs.configs import mcp_config_sse, mcp_config_stdio

dotenv.load_dotenv()

async def main():
    async with MCPClient(mcp_config_stdio) as client:
        try:
            tools = await client.get_tools()

            print("\033[1mAvailable tools:\033[0m")
            print(str([tool for tool in tools.keys()]))
            
            llm = ChatOpenAI(model="gpt-4.1")
            agent = Agent(
                name="HelloAgent",
                instruction="You are a helpful assistant that can calculate math problems using the provided tools.",
                llm=llm,
                tools=list(tools.values()),
                verbose=True
            )

            query = "What is the square root of ((2 + 3 * 2) ^ 2)?"
            print(f"\033[1mRunning agent with prompt\033[0m: {query}")
            response = await agent.arun(query)
            print(response)
        except Exception as e:
            print(f"\033[1mError: {e}\033[0m")

if __name__ == "__main__":
    asyncio.run(main())
