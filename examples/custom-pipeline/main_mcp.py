"""Example demonstrating the usage of gllm-plugin library for building a simple pipeline.

This module shows how to create and execute a basic pipeline using the gllm-plugin library.
It takes user input as a question and processes it through the pipeline to generate a response.
"""
from mcp_pipeline.mcp_config import get_mcp_servers
from gllm_agents.mcp.client import MCPClient
from mcp_pipeline.pipeline import McpPipelineBuilderPlugin
import asyncio


async def main():
    async with MCPClient(get_mcp_servers()) as mcp:
        pipeline_builder = McpPipelineBuilderPlugin()
        pipeline_config = {"mcp": mcp}
        pipeline = await pipeline_builder.build(pipeline_config)
        state = pipeline_builder.build_initial_state({"message": input("Question: ")}, {})
        result = await pipeline.invoke(
            initial_state=state, config={"user_multimodal_contents": []}
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
