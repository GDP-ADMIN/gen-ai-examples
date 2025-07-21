"""Standard RAG pipeline query processing utilities.

Authors:
    Surya Mahadi (made.r.s.mahadi@gdplabs.id)

References:
    NONE
"""

from typing import Any

from claudia_gpt.state import ClaudiaStateKeys as StateKeys


def concat_history_with_query(inputs: dict[str, Any]) -> str:
    """Prepend formatted conversation history to the user query.

    Includes the latest possible history messages without exceeding the prompt context character threshold.
    Only the latest messages that fit the threshold are included, in chronological order.

    Format:
        ```
        History:
        user: <user_message>
        assistant: <assistant_message>

        Query:
        <generation_query>
        ```
    Args:
        inputs (dict[str, Any]): The input dictionary containing the query and history.

    Returns:
        str: The combined *History + Query* string used by downstream steps.
    """
    # TODO: implement cascading history to support long chat history
    query: str = inputs[StateKeys.GENERATION_QUERY]
    history: list[tuple[str, list[Any]]] = inputs[StateKeys.HISTORY]
    prompt_context_char_threshold = inputs["prompt_context_char_threshold"]

    if not history:
        return query

    reversed_entries: list[str] = []
    total_len = len("History:\n") + len("\nQuery:\n") + len(query)

    for role, messages in reversed(history):
        if not messages:
            continue

        message = messages[0] if isinstance(messages, list) else messages  # type: ignore
        entry = f"{role}: {message}\n"

        if total_len + len(entry) > prompt_context_char_threshold:
            break

        reversed_entries.append(entry)
        total_len += len(entry)

    entries = reversed_entries[::-1]

    return "History:\n" + "".join(entries) + f"\nQuery:\n{query}"
