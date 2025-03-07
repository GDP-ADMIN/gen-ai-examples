"""Example demonstrating the usage of gllm-plugin library for building a simple pipeline.

This module shows how to create and execute a basic pipeline using the gllm-plugin library.
It takes user input as a question and processes it through the pipeline to generate a response.
"""

from simple_pipeline.pipeline import SimplePipelineBuilder
import asyncio

async def main():
    pipeline_builder = SimplePipelineBuilder()
    pipeline = pipeline_builder.build({})
    state = pipeline_builder.build_initial_state({"message": input("Question: ")}, {})
    result = await pipeline.invoke(state)
    response = result.get("response")
    print(f"Response:\n{response}")
    

if __name__ == "__main__":
    asyncio.run(main())