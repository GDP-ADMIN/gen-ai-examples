import asyncio
import dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

dotenv.load_dotenv()

def process_response(response, tool_name):
    print(f"\n=== Response from {tool_name} ===")
    print("Is a tool called?", bool(response["messages"][1].tool_calls))
    if response["messages"][1].tool_calls:
        print("Tool Called:", response["messages"][1].tool_calls[0]["name"])
    print("Output AIMessage:", response["messages"][-1].content)

async def main():
    async with MultiServerMCPClient(
        {
            "hello": {
                "command": "python",
                "args": ["mcp_tools/hello_tool_stdio.py"],
                "transport": "stdio",
            },
            "goodbye": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(
            "gpt-4o-mini",
            client.get_tools()
        )
        hello_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Say hello to World"}]}
        )
        goodbye_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Say goodbye to World"}]}
        )
        no_tool_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "What's going on?"}]}
        )
        
        # Process hello response
        process_response(hello_response, "hello")
        # Process goodbye response
        process_response(goodbye_response, "goodbye")
        # Process no tool response
        process_response(no_tool_response, "no tool")
        

if __name__ == "__main__":
    asyncio.run(main())
