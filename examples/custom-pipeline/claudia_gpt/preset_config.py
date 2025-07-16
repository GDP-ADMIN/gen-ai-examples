"""Base Pipeline Preset Config.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

from gllm_plugin.pipeline.base_pipeline_preset_config import BasePipelinePresetConfig
from pydantic import Field


class ClaudiaPresetConfig(BasePipelinePresetConfig):
    """A Pydantic model representing the preset configuration of a Standard RAG pipeline.

    Inherits attributes from `BasePipelinePresetConfig`.

    Attributes:
        normal_search_top_k (int): The top k for normal search. Must be greater than or equal to 1.
        retriever_top_k (int): The top k for retriever. Must be greater than or equal to 1.
        rerank_kwargs (str): The keyword arguments for reranking.
        rerank_type (str): The type of reranking.
    """

    normal_search_top_k: int = Field(ge=1)
    retriever_top_k: int = Field(ge=1)
    rerank_kwargs: str = "{}"
    rerank_type: str = ""
