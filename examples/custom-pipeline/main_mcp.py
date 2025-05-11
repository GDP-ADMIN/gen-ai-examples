"""Example demonstrating the usage of gllm-plugin library for building a simple pipeline.

This module shows how to create and execute a basic pipeline using the gllm-plugin library.
It takes user input as a question and processes it through the pipeline to generate a response.
"""
from mcp_pipeline.pipeline import McpPipelineBuilderPlugin
from simple_pipeline.pipeline import SimplePipelineBuilder
import asyncio


async def main():
    pipeline_builder = McpPipelineBuilderPlugin()
    pipeline_config = {}
    pipeline = pipeline_builder.build(pipeline_config)
    state = pipeline_builder.build_initial_state({"message": input("Question: ")}, {})
    await pipeline.invoke(
        initial_state=state, config={"user_multimodal_contents": []}
    )


if __name__ == "__main__":
    asyncio.run(main())
