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
3. Run `./run_example_stdio.sh` *or* `./run_example_sse.sh` (if you want to try either transport).

The final output should contain something like this for both:
```
Available tools:
['add', 'subtract', 'multiply', 'divide', 'square_root', 'power']

> Entering new AgentExecutor chain...

Invoking: `multiply` with `{'a': 3, 'b': 2}`


Processing request of type CallToolRequest
6
Invoking: `add` with `{'a': 2, 'b': 6}`


Processing request of type CallToolRequest
8
Invoking: `power` with `{'a': 8, 'b': 2}`


Processing request of type CallToolRequest
64
Invoking: `square_root` with `{'a': 64}`


Processing request of type CallToolRequest
8.0The square root of ((2 + 3 * 2) ^ 2) is 8.

> Finished chain.
{'input': 'What is the square root of ((2 + 3 * 2) ^ 2)?', 'output': 'The square root of ((2 + 3 * 2) ^ 2) is 8.'}
```
