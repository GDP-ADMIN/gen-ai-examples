"""Standard RAG pipeline caching utilities.

Authors:
    Surya Mahadi (made.r.s.mahadi@gdplabs.id)

References:
    NONE
"""

from claudia_gpt.utils.logger import logger


def is_prompt_within_context_limit(user_prompt: str, char_limit: int) -> bool:
    """Checks whether the user prompt is within the "context limit".

    If the prompt is longer than the character limit, it may be assumed that the user provides the context inside
    the prompt.

    Args:
        user_prompt (str): The user prompt.
        char_limit (int): The character limit.

    Returns:
        bool: Whether the user prompt is longer than the character limit.
    """
    is_within_limit = len(user_prompt) <= char_limit
    if not is_within_limit:
        logger.info(
            "User prompt is longer than the character limit. "
            "Assuming that the user provides the context inside the prompt."
        )
    return is_within_limit
