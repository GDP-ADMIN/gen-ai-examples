"""Base Pipeline Preset Config.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

from glchat_plugin.pipeline.base_pipeline_preset_config import BasePipelinePresetConfig


class ClaudiaPresetConfig(BasePipelinePresetConfig):
    """A Pydantic model representing the preset configuration of a Standard RAG pipeline.

    Inherits attributes from `BasePipelinePresetConfig`.

    Attributes:
        normal_search_top_k (int): The top k for normal search. Must be greater than or equal to 1.
        rerank_kwargs (str): The keyword arguments for reranking.
        rerank_type (str): The type of reranking.
    """

    normal_search_top_k: int = 20
    rerank_kwargs: str = "{}"
    rerank_type: str = "cohere"
