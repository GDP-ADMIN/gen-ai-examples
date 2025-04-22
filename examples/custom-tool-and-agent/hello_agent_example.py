# hello_agent_example.py
import os
from gllm_agents.agent.base import Agent
from langchain_openai import ChatOpenAI
# Import the custom tool from the other file
from hello_tool import SimpleHelloTool

# Initialize components
# Note: ChatOpenAI() will automatically look for the OPENAI_API_KEY env var.
llm = ChatOpenAI(model="gpt-4o")
tool = SimpleHelloTool()

# Create Agent
agent = Agent(
    name="HelloAgent",
    # Revert to simpler instruction
    instruction="You are a helpful assistant that can greet people by name using the provided tool.",
    llm=llm,
    tools=[tool],
    # Set verbose=True to see agent thoughts
    verbose=True
)

# Run Agent
query = "Please greet Raymond"
response = agent.run(query)

# Print the final output from the response dictionary
print(response['output'])

# Expected output format is now modified by the tool's return value
# Example: Tool says: Hello, Raymond! 