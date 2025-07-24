"""Example demonstrating the usage of gllm-plugin library for building a simple pipeline.

This module shows how to create and execute a basic pipeline using the gllm-plugin library.
It takes user input as a question and processes it through the pipeline to generate a response.
"""

import asyncio
import os
from typing import Any
from dotenv import load_dotenv

from gllm_inference.catalog import PromptBuilderCatalog

from simple_pipeline.pipeline import SimplePipelineBuilder


load_dotenv()


async def main():
    model_name = os.getenv("SIMPLE_PIPELINE_LANGUAGE_MODEL", "")
    lm_invoker_type, _ = model_name.split("/", 1)

    catalogs = {}
    catalog_records: list[dict[str, Any]] = [
        {
            "name": "generate_response",
            "system": "Answer the following question or follow these instructions:",
            "user": "{query}",
        }
    ]
    catalogs[""] = PromptBuilderCatalog.from_records(catalog_records)

    pipeline_builder = SimplePipelineBuilder()
    pipeline_builder.prompt_builder_catalogs = catalogs
    pipeline_config = {
        "model_name": model_name,
        "model_kwargs": {"lm_invoker_type": lm_invoker_type},
        "model_env_kwargs": {"credentials": "SIMPLE_PIPELINE_LLM_API_KEY"}
    }
    pipeline = await pipeline_builder.build(pipeline_config)
    state = pipeline_builder.build_initial_state({"message": input("Question: ")}, {})
    await pipeline.invoke(
        initial_state=state, config={"binaries": [], "hyperparameters": {}, "user_multimodal_contents": []}
    )


if __name__ == "__main__":
    asyncio.run(main())
