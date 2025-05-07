import os
from gllm_agents import Agent
from langchain_openai import ChatOpenAI
# Import the custom tool from the other file
from bosa_connectors import BOSAConnectorToolGenerator


# Initialize components
# Note: ChatOpenAI() will automatically look for the OPENAI_API_KEY env var.
llm = ChatOpenAI(model="gpt-4o")
bosa_connector_tool_generator = BOSAConnectorToolGenerator(
    api_base_url=os.getenv("BOSA_API_BASE_URL", "https://staging-api.bosa.id"),
    api_key=os.getenv("BOSA_API_KEY", ""),
    app_name="twitter",
)
tools = bosa_connector_tool_generator.generate_tools()

# Create Agent
agent = Agent(
    name="BOSAConnectorAgent",
    # Revert to simpler instruction
    instruction="You are a helpful assistant that use BOSA to connect with Twitter API.",
    llm=llm,
    tools=tools,
    # Set verbose=True to see agent thoughts
    verbose=True,
)

# Run AgentTwitter
query = "Please search twitter using BOSA by username elonmusk."
response = agent.run(query)

# Print the final output from the response dictionary
print(response['output'])

# Expected output format is now modified by the tool's return value
