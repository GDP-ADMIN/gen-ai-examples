"""Simple Pipeline Configuration.

Authors:
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)

References:
    None
"""

from typing import Any

from gllm_generation.response_synthesizer import StaticListResponseSynthesizer
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin

from simple_pipeline.preset_config import SimplePresetConfig
from simple_pipeline.state import SimpleState, SimpleStateKeys


class SimplePipelineBuilder(PipelineBuilderPlugin[SimpleState, SimplePresetConfig]):
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
        response_synthesizer_step = step(
            component=self.build_response_synthesizer(),
            input_state_map={
                "state_variables": SimpleStateKeys.RESPONSE_SYNTHESIS_BUNDLE
            },
            output_state=SimpleStateKeys.RESPONSE,
        )

        pipeline = Pipeline(
            steps=[
                response_synthesizer_step,
            ],
            state_type=SimpleState,
        )

        return pipeline

    def build_initial_state(self, request: dict[str, Any], pipeline_config: dict[str, Any], **kwargs: Any) -> SimpleState:
        """Build the initial state for pipeline invoke.

        Args:
            request (dict[str, Any]): The given request from the user.
            pipeline_config (dict[str, Any]): The pipeline configuration.
            **kwargs (Any): A dictionary of arguments required for building the initial state.

        Returns:
            SimpleState: The initial state.
        """
        return SimpleState(
            response_synthesis_bundle={"context_list": [f'{request.get("message")}']}
        )

    def build_response_synthesizer(self) -> StaticListResponseSynthesizer:
        """Build the response synthesizer component.

        Args:
            None

        Returns:
            StaticListResponseSynthesizer: The response synthesizer component.
        """
        response_prefix = (
            "Hello! I'm an AI assistant designed to help answer your questions. "
            "I'll do my best to provide clear and helpful information. "
            "Here's what you asked me: "
        )
        return StaticListResponseSynthesizer(response_prefix=response_prefix)
       

