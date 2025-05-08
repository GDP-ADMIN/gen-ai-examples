import asyncio
import dotenv

from gllm_agents import Agent
from gllm_agents.mcp.client import MCPClient
from langchain_openai import ChatOpenAI
from mcp_configs.configs import mcp_config_glchat_sse

dotenv.load_dotenv()

async def main():
    async with MCPClient(mcp_config_glchat_sse) as client:
        tools = client.get_tools()

        print("\033[1mAvailable tools:\033[0m")
        print(str([tool.name for tool in tools]))
        
        llm = ChatOpenAI(model="gpt-4.1")
        agent = Agent(
            name="HelloAgent",
            instruction="You are a helpful assistant that collaborate with GLChat, an AI chatbot that exposes MCP server. Show response from GLChat as is, do not rephrase it.",
            llm=llm,
            tools=tools,
            verbose=True
        )

        query = "What is the capital of Indonesia?"
        print(f"\033[1mRunning agent with prompt\033[0m: {query}")
        response = await agent.arun(query)
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
