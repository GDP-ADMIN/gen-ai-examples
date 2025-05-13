"""Simple Agentic Pipeline Configuration with MCP call.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import os
from enum import StrEnum

from dotenv import load_dotenv
from typing import Any, TypedDict

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import AgnosticPromptBuilder
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin
from gllm_generation.response_synthesizer import StuffResponseSynthesizer

from mcp_pipeline.preset_config import McpPresetConfig
from gllm_rag.preset.initializer import build_lm_invoker

load_dotenv(override=True)

class SimpleState(TypedDict):
    """A TypedDict representing the state of the Simple Pipeline.

    Attributes:
        query (str): The user's query.
        response (str): The generated response to the user's query.
    """

    query: str
    response: str



class SimpleStateKeys(StrEnum):
    """List of all possible keys in SimpleState."""

    QUERY = "query"
    RESPONSE = "response"

class McpPipelineBuilderPlugin(PipelineBuilderPlugin):
    """MCP Pipeline Builder Plugin.

    This pipeline will attempt to pass the user query to the response synthesizer,
    but utilizing tools that are provided by MCP Servers if needed.

    Inherits attributes from `PipelineBuilderPlugin`.
    """

    name = "mcp-pipeline"
    preset_config_class = McpPresetConfig

    async def build(self, pipeline_config: dict[str, Any]) -> Pipeline:
        """Build the pipeline.

        Args:
            pipeline_config (dict[str, Any]): The pipeline configuration.

        Returns:
            Pipeline: The simple pipeline.
        """
        mcp = pipeline_config["mcp"]
        tools = mcp.get_tools()
        invoker = build_lm_invoker(
            model_id=str(pipeline_config.get("model_name") or os.getenv("LANGUAGE_MODEL", "")),
            credentials=os.getenv(pipeline_config.get("api_key") or "LLM_API_KEY", ""),
            config={"tools": tools},
        )

        prompt_builder = AgnosticPromptBuilder(
            system_template="You are a helpful assistant that can use tools to calculate basic math problems.",
            user_template="{query}",
        )
        response_synthesizer = StuffResponseSynthesizer.from_lm_components(prompt_builder, invoker)
        response_synthesizer_step = step(
            component=response_synthesizer,
            input_state_map={
                "query": SimpleStateKeys.QUERY,
            },
            output_state=SimpleStateKeys.RESPONSE,
        )

        return Pipeline(
            steps=[response_synthesizer_step],
            state_type=SimpleState
        )

    def build_initial_state(
        self, request: dict[str, Any], pipeline_config: dict[str, Any], **kwargs: Any
    ) -> SimpleState:
        """Build the initial state for pipeline invoke.

        Args:
            request (dict[str, Any]): The given request from the user.
            pipeline_config (dict[str, Any]): The pipeline configuration.
            **kwargs (Any): A dictionary of arguments required for building the initial state.

        Returns:
            SimpleState: The initial state.
        """
        return SimpleState(query=request.get("message"), response=None)
