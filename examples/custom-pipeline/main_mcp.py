"""Example demonstrating the usage of gllm-plugin library for building a simple pipeline.

This module shows how to create and execute a basic pipeline using the gllm-plugin library.
It takes user input as a question and processes it through the pipeline to generate a response.
"""
import asyncio
import traceback

from dotenv import load_dotenv
from mcp_pipeline.pipeline import McpPipelineBuilderPlugin

load_dotenv()

async def main():
    pipeline_builder = McpPipelineBuilderPlugin()

    pipeline_configs = [
        {"model_name": "openai/gpt-4o-mini"},
        {"model_name": "openai/gpt-4o"},
    ]

    pipelines = {}
    for pipeline_config in pipeline_configs:
        pipeline = await pipeline_builder.build(pipeline_config)
        pipelines[pipeline_config["model_name"]] = pipeline

    print("Select a model:")
    for i, model_name in enumerate(pipelines.keys()):
        print(f"- {i + 1}. {model_name}")

    model_input = input("Select a model (default: GPT-4o): ")
    try:
        model_index = int(model_input) - 1 if model_input.strip() else 1
        if model_index < 0 or model_index >= len(pipelines):
            print(f"Invalid selection, using default model (GPT-4o)")
            model_index = 1
    except ValueError:
        print(f"Invalid input, using default model (GPT-4o)")
        model_index = 1
        
    selected_model = list(pipelines.keys())[model_index]
    print(f"Using model: {selected_model}")
    
    state = pipeline_builder.build_initial_state({"message": input("Question: ")}, {})
    try:
        result = await pipelines[selected_model].invoke(
            initial_state=state, config={"user_multimodal_contents": []}
        )
        print(result)
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}")
    finally:
        await pipeline_builder.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
