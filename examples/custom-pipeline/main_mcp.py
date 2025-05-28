"""Example demonstrating the usage of gllm-plugin library for building a simple pipeline.

This module shows how to create and execute a basic pipeline using the gllm-plugin library.
It takes user input as a question and processes it through the pipeline to generate a response.
"""
import asyncio
import os
from dotenv import load_dotenv
from mcp_pipeline.pipeline import McpPipelineBuilderPlugin

load_dotenv()

async def main():
    pipeline_builder = McpPipelineBuilderPlugin()
    
    model_name = os.getenv("LANGUAGE_MODEL", "openai/gpt-4.1")
    api_key = os.getenv("LLM_API_KEY", "")
    pipeline_config = {"model_name": model_name, "api_key": api_key, "mcp_server_url": "MCP_SERVER_URL"}
    pipeline = await pipeline_builder.build(pipeline_config)
    state = pipeline_builder.build_initial_state({"message": input("Question: ")}, {})
    response = await pipeline.invoke(
        initial_state=state, config={"user_multimodal_contents": []}
    )
    print()
    print("Response:\n")
    print(response['response'])

if __name__ == "__main__":
    asyncio.run(main())
