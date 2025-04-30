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
['text_frequency_counter', 'sort_frequencies', 'to_json']


> Entering new AgentExecutor chain...

Invoking: `text_frequency_counter` with `{'text': 'a a a a b b c c c d d e e e e f f f g g g h h i i j j j k k l l l m m n n o o o o o p p q r r r s s s s t t u u v v w x y z'}`


Processing request of type CallToolRequest
{"a": 4, "b": 2, "c": 3, "d": 2, "e": 4, "f": 3, "g": 3, "h": 2, "i": 2, "j": 3, "k": 2, "l": 3, "m": 2, "n": 2, "o": 5, "p": 2, "q": 1, "r": 3, "s": 4, "t": 2, "u": 2, "v": 2, "w": 1, "x": 1, "y": 1, "z": 1}
Invoking: `sort_frequencies` with `{'frequencies': {'a': 4, 'b': 2, 'c': 3, 'd': 2, 'e': 4, 'f': 3, 'g': 3, 'h': 2, 'i': 2, 'j': 3, 'k': 2, 'l': 3, 'm': 2, 'n': 2, 'o': 5, 'p': 2, 'q': 1, 'r': 3, 's': 4, 't': 2, 'u': 2, 'v': 2, 'w': 1, 'x': 1, 'y': 1, 'z': 1}}`


Processing request of type CallToolRequest
{"o": 5, "a": 4, "e": 4, "s": 4, "c": 3, "f": 3, "g": 3, "j": 3, "l": 3, "r": 3, "b": 2, "d": 2, "h": 2, "i": 2, "k": 2, "m": 2, "n": 2, "p": 2, "t": 2, "u": 2, "v": 2, "q": 1, "w": 1, "x": 1, "y": 1, "z": 1}
Invoking: `to_json` with `{'data': {'o': 5, 'a': 4, 'e': 4, 's': 4, 'c': 3}}`


Processing request of type CallToolRequest
{"o": 5, "a": 4, "e": 4, "s": 4, "c": 3}{"o": 5, "a": 4, "e": 4, "s": 4, "c": 3}

> Finished chain.
{'input': "\n            What are the top 5 frequent words in the text 'a a a a b b c c c d d e e e e f f f g g g h h i i j j j k k\n            l l l m m n n o o o o o p p q r r r s s s s t t u u v v w x y z'\n\n            Output should *only* be the JSON string of the dictionary of words and their frequencies.\n        ", 'output': '{"o": 5, "a": 4, "e": 4, "s": 4, "c": 3}'}
```
