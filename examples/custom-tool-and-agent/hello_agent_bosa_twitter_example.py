# hello_agent_example.py
from gllm_agents import Agent
from langchain_openai import ChatOpenAI
# Import the custom tool from the other file
from bosa_twitter_tool import BosaTwitterTool

# Initialize components
# Note: ChatOpenAI() will automatically look for the OPENAI_API_KEY env var.
llm = ChatOpenAI(model="gpt-4o")
twitter_tool = BosaTwitterTool()

# Create Agent
agent = Agent(
    name="BOSAConnectorTwitterAgent",
    # Revert to simpler instruction
    instruction="You are a helpful assistant that use BOSA to connect with Twitter API.",
    llm=llm,
    tools=[twitter_tool],
    # Set verbose=True to see agent thoughts
    verbose=True
)

# Run Agent
query = "Please search twitter using BOSA by username elonmusk."
response = agent.run(query)

# Print the final output from the response dictionary
print(response['output'])

# Expected output format is now modified by the tool's return value
# Example: 
# The search for the username "elonmusk" on Twitter using BOSA returned the following result:
#- **Name**: gorklon rust
#- **Username**: elonmusk
#- **User ID**: 44196397
