"""Module responsible for transforming user queries using the chat history context and expanding abbreviations.

Author:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from typing import Any

from gllm_core.schema import Component

# from claudia_gpt.constant.agent_type import AgentType
# from claudia_gpt.query_transformer.abbreviation.abbreviation_config_loader import DatabaseAbbreviationConfigLoader
# from claudia_gpt.query_transformer.catapa_use_case_query_transformer import CatapaUseCaseQueryTransformer


# TODO: Use `BaseQueryTransformer` from `gllm_retrieval`
class CatapaQueryTransformer(Component):
    """Class responsible for transforming user queries using the chat history context and expanding abbreviations.

    Attributes:
        query_transformers (CatapaUseCaseQueryTransformer): The query transformer for the Catapa use case.
    """

    def __init__(self):
        """Initialize the CatapaQueryTransformer."""
        # abbreviation_dict = DatabaseAbbreviationConfigLoader().get_abbreviation_dict()
        # self.query_transformers = CatapaUseCaseQueryTransformer(abbreviation_dict[AgentType.HELP_CENTER_CATAPA.value])

    async def _run(self, query: str, **kwargs: Any) -> str:
        """Run the chat history manager component.

        Args:
            query (str): The query to be transformed.
            kwargs (Any): The keyword arguments, which may contain the operation.

        Returns:
            str: The transformed query.
        """
        # result = await self.query_transformers.transform_query(
        #     original_query=query, chat_history=kwargs.get("chat_history", [])
        # )

        # return result
        return query
