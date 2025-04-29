# Custom Tool and Agent Hello World

Check the step-by-step sample to create custom tool and agent in https://glair.gitbook.io/hello-world

## Running MCP Tools on AI Agents

The project also contains AI Agents that utilize the power of [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction).

### Pre-requisites
1. Python 3.11 or 3.12.
2. Poetry (`pip install poetry`)

### Setting up and Execution
1. Run `poetry install`
2. Add `.env` your api key (i.e., `OPENAI_API_KEY`)
3. Run `./run_example.sh`

The final output should look something like this:
```
=== Response from hello ===
Is a tool called? True
Tool Called: hello_tool
Output AIMessage: Hello, World!

=== Response from goodbye ===
Is a tool called? True
Tool Called: goodbye_tool
Output AIMessage: Goodbye, World!

=== Response from no tool ===
Is a tool called? False
Output AIMessage: Hello! I'm here to help you with any questions or tasks you have. How can I assist you today?
```
