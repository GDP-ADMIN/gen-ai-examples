# Custom Tool and Agent Hello World
This is an example how to create custom tool and agent.

## 1. Tool Development Guide

### Creating Basic Tools with the Decorator

The simplest way to create a new tool is using the `@tool_plugin` decorator:

```python
from typing import Any
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from gdplabs_gen_ai_starter_gllm_backend.gllm_agents.plugins import tool_plugin

# Input schema definition
class GreetingInput(BaseModel):
    """Input schema for the greeting tool."""
    name: str = Field(..., description="Name to greet")

# Tool implementation with decorator
@tool_plugin(version="1.0.0")
class GreetingTool(BaseTool):
    """A simple greeting tool implementation."""

    name: str = "greeting"
    description: str = "Generates a greeting message for the provided name"
    args_schema: type[BaseModel] = GreetingInput

    def _run(self, name: str, **kwargs: Any) -> str:
        """Run the greeting tool."""
        return f"Hello, {name}! Welcome to the tool plugin system."
```

This pattern enables a clean, declarative style for tool creation with minimal boilerplate.

### Input Schema Definition

Tools use Pydantic models to define and validate input parameters:

```python
class CalculatorInput(BaseModel):
    """Input schema for a calculator tool."""

    operation: str = Field(
        ...,
        description="Mathematical operation (add, subtract, multiply, divide)"
    )
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")
```

Key benefits of this approach:
- **Automatic validation**: Input types are checked automatically
- **Self-documenting**: Fields include descriptions for documentation
- **Default values**: Optional parameters can have default values
- **Rich validation**: Complex validation rules can be applied

### Tool Implementation Patterns

The core of any tool is its `_run` method, which implements the tool's functionality:

```python
def _run(self, operation: str, a: float, b: float, **kwargs: Any) -> str:
    """Run the calculator tool."""

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

    return f"Result of {a} {operation} {b} = {result}"
```

Best practices for the `_run` method:
- Return string results for best compatibility with agents
- Handle all expected errors gracefully
- Provide clear error messages for debugging
- Document parameters and return values

### Error Handling and Parameter Validation

Robust error handling is crucial for tools:

```python
def _run(self, query: str, **kwargs: Any) -> str:
    """Run the search tool."""

    try:
        # Validate input
        if not query or len(query.strip()) < 3:
            return "Query must be at least 3 characters long"

        # Execute search
        results = self._search_service.search(query)

        # Format results
        if not results:
            return "No results found for your query."

        return self._format_results(results)

    except ConnectionError:
        return "Error: Could not connect to search service. Please try again later."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
```

This pattern ensures that:
- Invalid inputs are caught early
- Expected exceptions are handled gracefully
- Unexpected errors are reported clearly
- The agent receives useful feedback
