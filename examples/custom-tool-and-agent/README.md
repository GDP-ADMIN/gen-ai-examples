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
> Entering new AgentExecutor chain...

Invoking: `hello_tool` with `{'name': 'World'}`


Processing request of type CallToolRequest
Hello, World!Hello, World!

> Finished chain.


> Entering new AgentExecutor chain...

Invoking: `goodbye_tool` with `{'name': 'World'}`


Goodbye, World!Goodbye, World!

> Finished chain.


> Entering new AgentExecutor chain...
I'm here to help you! How can I assist you today? If you need me to say hello or goodbye to someone by name, just let me know!

> Finished chain.
{'input': 'Say hello to World', 'output': 'Hello, World!'}
{'input': 'Say goodbye to World', 'output': 'Goodbye, World!'}
{'input': "What's going on?", 'output': "I'm here to help you! How can I assist you today? If you need me to say hello or goodbye to someone by name, just let me know!"}
```
