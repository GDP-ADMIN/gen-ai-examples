import asyncio
import dotenv

from gllm_agents import Agent
from langchain_openai import ChatOpenAI
from mcp_client import MCPClient
from mcp_configs.configs import mcp_config_sse

dotenv.load_dotenv()

async def main():
    client = MCPClient(mcp_config_sse)

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

        response = await agent.arun("""
            What are the top 5 frequent words in the text 'a a a a b b c c c d d e e e e f f f g g g h h i i j j j k k
            l l l m m n n o o o o o p p q r r r s s s s t t u u v v w x y z'

            Output should *only* be the JSON string of the dictionary of words and their frequencies.
        """)
        print(response)

    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
