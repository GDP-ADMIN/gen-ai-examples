"""Simple Agentic Pipeline Configuration with MCP call.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import os
from enum import StrEnum

from dotenv import load_dotenv
from typing import Any, TypedDict

from gllm_generation.response_synthesizer import StuffResponseSynthesizer
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin
from gllm_rag.preset.lm import LM, LMState

from mcp_pipeline.preset_config import McpPresetConfig
from mcp_pipeline.response_synthesizer import McpResponseSynthesizer

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

    def build(self, pipeline_config: dict[str, Any]) -> Pipeline:
        """Build the pipeline.

        Args:
            pipeline_config (dict[str, Any]): The pipeline configuration.

        Returns:
            Pipeline: The simple pipeline.
        """
        # model_name = str(pipeline_config.get("model_name") or os.getenv("LANGUAGE_MODEL", ""))
        # api_key = os.getenv(pipeline_config.get("api_key") or "LLM_API_KEY", "")
        # self.lm = LM(
        #     language_model_id=model_name,
        #     language_model_credentials=api_key,
        # )

        response_synthesizer_step = step(
            component=McpResponseSynthesizer(),
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
        return SimpleState(
            query=request.get("message"),
        )
