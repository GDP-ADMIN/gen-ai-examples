"""Simple Pipeline Configuration.

Authors:
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)

References:
    None
"""

import os
from dotenv import load_dotenv
from typing import Any

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin
from gllm_rag.preset.lm import LM, LMState
from simple_pipeline.preset_config import SimplePresetConfig

load_dotenv()


class SimplePipelineBuilder(PipelineBuilderPlugin[LMState, SimplePresetConfig]):
    """Simple pipeline builder.

    This pipeline will simply pass the user query to the response synthesizer.
    There are no prompt templates used in this pipeline.

    Inherits attributes from `PipelineBuilderPlugin`.
    """

    name = "simple-pipeline"
    preset_config_class = SimplePresetConfig

    def __init__(self):
        """Initialize the simple pipeline builder."""
        super().__init__()

    def build(self, pipeline_config: dict[str, Any]) -> Pipeline:
        """Build the pipeline.

        Args:
            pipeline_config (dict[str, Any]): The pipeline configuration.

        Returns:
            Pipeline: The simple pipeline.
        """
        model_name = str(pipeline_config.get("model_name") or os.getenv("LANGUAGE_MODEL", ""))
        api_key = os.getenv(pipeline_config.get("api_key") or "OPENAI_API_KEY", "")
        self.lm = LM(
            language_model_id=model_name,
            language_model_credentials=api_key,
        )
        return self.lm.build()

    def build_initial_state(
        self, request: dict[str, Any], pipeline_config: dict[str, Any], **kwargs: Any
    ) -> LMState:
        """Build the initial state for pipeline invoke.

        Args:
            request (dict[str, Any]): The given request from the user.
            pipeline_config (dict[str, Any]): The pipeline configuration.
            **kwargs (Any): A dictionary of arguments required for building the initial state.

        Returns:
            LMState: The initial state.
        """
        return self.lm.build_initial_state(
            query=request.get("message"),
            config={"event_emitter": kwargs.get("event_emitter")},
        )
