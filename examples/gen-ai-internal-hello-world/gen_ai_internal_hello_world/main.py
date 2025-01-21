"""Main module for the gen_ai_hello_world application that handles RAG operations and pipeline building.

This is an example of how to use the gllm-pipeline library to build a RAG pipeline.
We utilize CustomDataStore for simplicity.
It's to mock the data store so you don't need to have an Elasticsearch instance to run this example.
In production, you should use other implementation of DataStore.
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_generation.response_synthesizer import StuffResponseSynthesizer
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import OpenAIPromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_misc.context_manipulator import Repacker
from gllm_pipeline.steps import BundlerStep, step
from gllm_retrieval.retriever import BasicRetriever
from gen_ai_internal_hello_world.custom_data_store import CustomDataStore

SYSTEM_PROMPT = """
You are an AI assistant.
Answer the user query below based on the context.

**CONTEXT**
{context}
"""
USER_PROMPT = "{query}"


def build_retriever():
    """Build a retriever for the pipeline."""
    data_store = CustomDataStore()
    return BasicRetriever(data_store)


def build_repacker():
    """Build a repacker for the pipeline."""
    return Repacker(mode="context")


def build_response_synthesizer():
    """Build a response synthesizer for the pipeline."""
    prompt_builder = OpenAIPromptBuilder(SYSTEM_PROMPT, USER_PROMPT)
    lm_invoker = OpenAILMInvoker(os.getenv("LANGUAGE_MODEL"), os.getenv("OPENAI_API_KEY"))
    lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
    return StuffResponseSynthesizer(lm_request_processor)


def build_pipeline():
    """Build a pipeline for the gen_ai_hello_world application."""
    retriever_step = step(build_retriever(), {"query": "user_query"}, "chunks", {"top_k": "top_k"})
    repacker_step = step(build_repacker(), {"chunks": "chunks"}, "context")
    bundler_step = BundlerStep("create_rs_bundle", ["context"], "response_synthesis_bundle")
    response_synthesizer_step = step(
        build_response_synthesizer(),
        {"query": "user_query", "variables": "response_synthesis_bundle"},
        "response",
    )

    return retriever_step | repacker_step | bundler_step | response_synthesizer_step


def main():
    """Main function to run the gen_ai_hello_world application."""
    load_dotenv()
    e2e_pipeline = build_pipeline()
    state = {"user_query": input("Question: ")}
    config = {"top_k": 4}
    result = asyncio.run(e2e_pipeline.invoke(state, config))
    response = result.get("response")
    print(f"Response:\n{response}")


if __name__ == "__main__":
    main()
