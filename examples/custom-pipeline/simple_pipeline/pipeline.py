"""Simple Pipeline Configuration.

Authors:
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)

References:
    None
"""

from typing import Any

from gllm_generation.response_synthesizer import StuffResponseSynthesizer
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin
from gllm_plugin.utils.get_catalog import get_catalog
from gllm_plugin.utils.get_lm_invoker import get_lm_invoker

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

    async def build(self, pipeline_config: dict[str, Any]) -> Pipeline:
        """Build the pipeline.

        Args:
            pipeline_config (dict[str, Any]): The pipeline configuration.

        Returns:
            Pipeline: The simple pipeline.
        """
        model_name = pipeline_config.get("model_name")
        model_kwargs = pipeline_config.get("model_kwargs", {})
        model_env_kwargs = pipeline_config.get("model_env_kwargs", {})

        response_synthesizer_step = step(
            component=self.build_response_synthesizer(model_name, model_kwargs, model_env_kwargs),
            input_state_map={
                "query": SimpleStateKeys.QUERY,
                "event_emitter": SimpleStateKeys.EVENT_EMITTER,
            },
            output_state=SimpleStateKeys.RESPONSE,
            runtime_config_map={
                "user_multimodal_contents": "binaries",
                "hyperparameters": "hyperparameters",
            },
        )

        pipeline = Pipeline(
            steps=[
                response_synthesizer_step,
            ],
            state_type=SimpleState,
        )

        return pipeline

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
            response=None,
            event_emitter=kwargs.get("event_emitter")
        )

    def build_response_synthesizer(
        self, model_name: str, model_kwargs: dict[str, Any], model_env_kwargs: dict[str, Any]
    ) -> StuffResponseSynthesizer:
        """Build the response synthesizer component.

        Args:
            model_name (str): The model to use for inference.
            model_kwargs (dict[str, Any]): The model kwargs.
            model_env_kwargs (dict[str, Any]): The model env kwargs.

        Returns:
            StuffResponseSynthesizer: The response synthesizer component.
        """
        lm_invoker = get_lm_invoker(model_name, model_kwargs, model_env_kwargs)
        prompt_builder = get_catalog(self.prompt_builder_catalogs, "generate_response", model_name)
        response_synthesizer = StuffResponseSynthesizer.from_lm_components(prompt_builder, lm_invoker)
        return response_synthesizer
