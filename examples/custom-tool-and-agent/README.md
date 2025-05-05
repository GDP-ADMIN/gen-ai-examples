# Custom Tool and Agent Hello World

Check the step-by-step sample to create custom tool and agent in https://glair.gitbook.io/hello-world

## Running MCP Tools on AI Agents

The project also contains AI Agents that utilize the power of [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction).

### Pre-requisites

1. Python 3.11 or 3.12.
2. Poetry (`pip install poetry`)

### Setting up and Execution

1. Add `.env` your api key (i.e., `OPENAI_API_KEY`)
2. Run `./run_example_stdio.sh` _or_ `./run_example_sse.sh` (if you want to try either transport).
   a. When running SSE script, we expect port `8000` to be free; otherwise, you will be informed, and the execution will be aborted.

The final output should contain something like this for both:

```
Available tools:
['add', 'subtract', 'multiply', 'divide', 'square_root', 'power']
Running agent with prompt: What is the square root of ((2 + 3 * 2) ^ 2)?


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

3. You can also run `run_example_glchat.sh` (you need to enable GDP Labs VPN for this to work) to run the example with GLChat agent. The output will be something like this:

```
Available tools:
['message']
Running agent with prompt: Tell me a short funny story

> Entering new AgentExecutor chain...

Invoking: `message` with `{'prompt': 'What is the capital of Indonesia?'}`


The capital of Indonesia is Jakarta.
The capital of Indonesia is Jakarta.

> Finished chain.
{'input': 'What is the capital of Indonesia?', 'output': 'The capital of Indonesia is Jakarta.'}
```

### Customizing MCP Servers

In the [mcp_configs/configs.py](mcp_configs/configs.py) file, you can customize the MCP servers. You can add more or remove MCP Servers as per your requirements.

Defining an MCP Server requires the `transport` to be defined. It is one of:

- `stdio`
- `sse`

**Note that HTTP Streams are not supported for Python yet.**

#### STDIO Server

An STDIO server is a server that uses the standard input and output to communicate with the MCP.

```python
{
    "tool_name": {
        "command": "python",
        "args": ["mcp_tools/tool_name.py"],
        "transport": "stdio",
    }
}
```

`command` can be one of (but not limited to)

- `python`
- `npx`
- `docker`

`args` is a list of arguments to pass to the command.

#### SSE Servers

An SSE server is a server that uses the Server-Sent Events (SSE) to communicate with the MCP. It simply needs a URL to the SSE endpoint. Typically, this ends in `/sse`.

```python
{
    "tool_name": {
        "url": "http://localhost:8000/sse",
        "transport": "sse",
    }
}
```

#### Example

An example of multiple MCP servers is as follows:

```python
mcp_config = {
    "math_tools": {
        "command": "python",
        "args": ["mcp_tools/math_tools_stdio.py"],
        "transport": "stdio",
    },
    "bosa_github": {
        "url": "https://api.bosa.id/sse/github",
        "transport": "sse",
    },
}
```
