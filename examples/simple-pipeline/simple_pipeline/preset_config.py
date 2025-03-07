"""Base Pipeline Preset Config.

Authors:
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)

References:
    NONE
"""

from gllm_plugin.pipeline.base_pipeline_preset_config import BasePipelinePresetConfig


class SimplePresetConfig(BasePipelinePresetConfig):
    """A Pydantic model representing the preset config of a No-op pipeline.

    Inherits attributes from `BasePipelinePresetConfig`.

    Attributes:
        None
    """