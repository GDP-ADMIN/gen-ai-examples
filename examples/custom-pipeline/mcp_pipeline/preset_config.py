"""Base Pipeline Preset Config.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

from gllm_plugin.pipeline.base_pipeline_preset_config import BasePipelinePresetConfig


class McpPresetConfig(BasePipelinePresetConfig):
    """A Pydantic model representing the preset config of a simple pipeline.

    Inherits attributes from `BasePipelinePresetConfig`.
    """
