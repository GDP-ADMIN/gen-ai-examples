"""Pipeline helper base class.

Authors:
    Ryan Ignatius Hadiwijaya (ryan.i.hadiwijaya@gdplabs.id)

References:
    None
"""

import json
from typing import Any

from gllm_inference.catalog import LMRequestProcessorCatalog
from gllm_inference.catalog.catalog import BaseCatalog
from gllm_inference.prompt_builder.prompt_builder import BasePromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_pipeline.steps import step
from gllm_pipeline.steps.pipeline_step import BasePipelineStep

from claudia_gpt.chat_history.schemas import DocumentStatus
from claudia_gpt.component.chat_history_manager import ChatHistoryManager
from claudia_gpt.utils.logger import logger

DEFAULT_SCOPE = ""


def get_retrieval_params(request: dict[str, Any]) -> dict[str, Any]:
    """Get the retrieval parameters from the request.

    The params is used to retrieve the uploaded document chunks of conversation.

    Args:
        request (dict[str, Any]): The request object.

    Returns:
        dict[str, Any]: The retrieval parameters.
    """
    retrieval_params: dict[str, Any] = {
        "filters": {
            "bool": {
                "should": [
                    {"bool": {"must_not": {"exists": {"field": "metadata.conversation_id"}}}},
                ],
                "minimum_should_match": 1,
            }
        }
    }

    if request.get("conversation_id"):
        retrieval_params["filters"]["bool"]["should"].append(
            {"term": {"metadata.conversation_id.keyword": request.get("conversation_id")}},
        )

    return retrieval_params


def to_bool(value: Any) -> bool:
    """Convert value to boolean.

    Values from Google Spreadsheet are in string format, so we need to convert them to boolean.
    "0" is truthy value, so we need to handle it separately.

    Args:
        value (Any): The value to convert.

    Returns:
        bool: The converted value.
    """
    if isinstance(value, str):
        return value.strip().lower() not in ["0", "false", "no", "n", ""]
    return bool(value)


def build_save_history_step(
    chat_history_manager: ChatHistoryManager,
    name: str | None = None,
    additional_input_state_map: dict[str, str] | None = None,
    output_state: str = "history",
    additional_runtime_config_map: dict[str, str] | None = None,
) -> BasePipelineStep:
    """Build the default save history step.

    Args:
        chat_history_manager (ChatHistoryManager): The chat history manager.
        name (str | None): The name of the step.
        additional_input_state_map (dict[str, str] | None): Additional input state map
            to be merged with the default input state map.
            This map will be prioritized over the default map. For example, using this:
            ```python
            additional_input_state_map = {
                ChatHistoryManager.QUERY_KEY: "new_query",
                ChatHistoryManager.REFERENCE_KEY: "new_reference",
            }
            ```
            will results in the following:
            ```python
            input_state_map = {
                ChatHistoryManager.QUERY_KEY: "new_query",
                ChatHistoryManager.RESPONSE_KEY: "response",
                ChatHistoryManager.REFERENCE_KEY: "new_reference",
            }
            ```
        output_state (str): The output state, default to "history".
        additional_runtime_config_map (dict[str, str] | None): Additional runtime config map
            to be merged with the default runtime config map.
            This map will be prioritized over the default map. For example, using this:
            ```python
            additional_runtime_config_map = {
                ChatHistoryManager.USER_ID_KEY: "new_user_id",
                ChatHistoryManager.SEARCH_TYPE_KEY: "search_type",
            }
            ```
            will results in the following:
            ```python
            runtime_config_map = {
                ChatHistoryManager.USER_ID_KEY: "new_user_id",
                ChatHistoryManager.CONVERSATION_ID_KEY: "conversation_id",
                ChatHistoryManager.PARENT_ID_KEY: "parent_id",
                ChatHistoryManager.USER_MESSAGE_ID_KEY: "user_message_id",
                ChatHistoryManager.ASSISTANT_MESSAGE_ID_KEY: "assistant_message_id",
                ChatHistoryManager.SOURCE_KEY: "source",
                ChatHistoryManager.ATTACHMENTS_KEY: "attachments",
                ChatHistoryManager.SEARCH_TYPE_KEY: "search_type",
            }
            ```

    Returns:
        BasePipelineStep: The save history step.
    """
    from claudia_gpt.config.pipeline.general_pipeline_config import (
        GeneralPipelineConfigKeys,
    )

    default_input_state_map = {
        ChatHistoryManager.QUERY_KEY: "query",
        ChatHistoryManager.RESPONSE_KEY: "response",
        ChatHistoryManager.EVENT_EMITTER_KEY: "event_emitter",
    }
    default_runtime_config_map = {
        ChatHistoryManager.USER_ID_KEY: GeneralPipelineConfigKeys.USER_ID,
        ChatHistoryManager.CONVERSATION_ID_KEY: GeneralPipelineConfigKeys.CONVERSATION_ID,
        ChatHistoryManager.PARENT_ID_KEY: GeneralPipelineConfigKeys.PARENT_ID,
        ChatHistoryManager.USER_MESSAGE_ID_KEY: GeneralPipelineConfigKeys.USER_MESSAGE_ID,
        ChatHistoryManager.ASSISTANT_MESSAGE_ID_KEY: GeneralPipelineConfigKeys.ASSISTANT_MESSAGE_ID,
        ChatHistoryManager.SOURCE_KEY: GeneralPipelineConfigKeys.SOURCE,
        ChatHistoryManager.ATTACHMENTS_KEY: GeneralPipelineConfigKeys.ATTACHMENTS,
    }
    return step(
        name=name,
        component=chat_history_manager,
        input_state_map=default_input_state_map | (additional_input_state_map or {}),
        output_state=output_state,
        runtime_config_map=default_runtime_config_map | (additional_runtime_config_map or {}),
        fixed_args={ChatHistoryManager.OPERATION_KEY: ChatHistoryManager.OP_WRITE},
    )


def check_dpo_success(inputs: dict[str, Any]) -> bool:
    """Check if the DPO successfully processes all the attachments and URLs.

    Args:
        inputs (dict[str, Any]): Dictionary containing the states of the pipeline. Must contain the `attachments` and
            `processed_urls` keys.

    Returns:
        bool: Whether the DPO successfully processes all the attachments and URLs.
    """
    attachments = inputs["attachments"].get("attachments", [])
    processed_urls = inputs["processed_urls"]
    attachment_error = any(attachment.get("status") != DocumentStatus.DONE.value for attachment in attachments)
    url_error = any(url.get("status") != DocumentStatus.DONE.value for url in processed_urls)
    return not attachment_error and not url_error


def create_attachment_retrieval_params(inputs: dict[str, Any]) -> dict[str, Any]:
    """Create the retrieval parameters for the attachments.

    Args:
        inputs (dict[str, Any]): Dictionary containing the states of the pipeline. Must contain the `retrieval_params`
            and `attachments` keys.

    Returns:
        dict[str, Any]: Extended retrieval parameters with file_id filters.
    """
    retrieval_params = inputs.get("retrieval_params", {})
    processed_urls = inputs.get("processed_urls", [])
    attachments: dict[str, list[dict[str, Any]]] = inputs.get("attachments", {})
    actual_attachments = attachments.get("attachments", [])

    file_ids = [file["id"] for file in actual_attachments] + [url["file_id"] for url in processed_urls]
    file_id_filter = {"terms": {"metadata.file_id.keyword": file_ids}}

    if retrieval_params:
        retrieval_params["filters"]["bool"]["must"] = [file_id_filter]
    else:
        retrieval_params = {"filters": {"bool": {"must": [file_id_filter]}}}

    return retrieval_params


def get_lmrp_by_scope(catalogs: LMRequestProcessorCatalog, name: str, scope: str = "") -> LMRequestProcessor:
    """Get the LM Request Processor from the catalog based on the scope.

    Args:
        catalogs (dict[str, BaseCatalog[Any]]): The catalogs to search in.
        name (str): The name of the LM Request Processor.
        scope (str, optional): The catalog scope. Defaults to "".

    Returns:
        LMRequestProcessor: The LM Request Processor.

    Raises:
        ValueError: If the name is not found in any catalog.
    """
    return _get_by_scope(catalogs, name, scope)


def get_prompt_builder_by_scope(
    catalogs: dict[str, BaseCatalog[Any]], prompt_id: str, scope: str = ""
) -> BasePromptBuilder:
    """Get the prompt builder from the catalog based on the scope.

    Args:
        catalogs (dict[str, BaseCatalog[Any]]): The catalogs to search in.
        prompt_id (str): The prompt ID.
        scope (str, optional): The catalog scope. Defaults to "".

    Returns:
        BasePromptBuilder: The prompt builder.

    Raises:
        ValueError: If the prompt ID is not found in any catalog.
    """
    return _get_by_scope(catalogs, prompt_id, scope)


def _get_by_scope(
    catalogs: dict[str, BaseCatalog[Any]], identifier: str, scope: str = ""
) -> BasePromptBuilder | LMRequestProcessor:
    """Get the prompt builder from the catalog based on the scope.

    The scope could be a model name (eg: openai/gpt-4o-mini), a provider name (eg: openai), or an empty string.

    This function will do the following:
    - If the exact scope is found in catalogs, and identifier is in the scope's catalog, return the prompt builder.
    - Otherwise, it will extract the provider name from the scope, and try to find again in the catalogs.
    - If still not found, it will try to find the prompt builder in the default catalog (denoted by empty string).
    - It will raise ValueError if the prompt ID is not found in any catalog.

    Args:
        catalogs (dict[str, BaseCatalog[Any]]): The catalogs to search in.
        identifier (str): The prompt ID or name.
        scope (str, optional): The catalog scope. Defaults to "".

    Returns:
        BasePromptBuilder: The prompt builder.

    Raises:
        ValueError: If the prompt ID is not found in any catalog.
    """
    builder = _get_from_catalogs(catalogs, identifier, scope)

    if builder is None and "/" in scope:
        builder = _get_from_catalogs(catalogs, identifier, scope.split("/")[0])

    if builder is None:
        builder = _get_from_catalogs(catalogs, identifier, DEFAULT_SCOPE)

    if builder is None:
        raise ValueError(f"Prompt builder `{identifier}` not found in any catalog.")

    return builder


def _get_from_catalogs(
    catalogs: dict[str, BaseCatalog[Any]], identifier: str, scope: str = ""
) -> BasePromptBuilder | LMRequestProcessor | None:
    """Get the prompt builder or LM Request Processor for the scope.

    Args:
        catalogs (dict[str, BaseCatalog[Any]]): The catalogs.
        identifier (str): The prompt ID or name.
        scope (str, optional): The scope. Defaults to "".

    Returns:
        BasePromptBuilder | LMRequestProcessor | None: The prompt builder or LM Request Processor, or None if not found.
    """
    if scope in catalogs and identifier in catalogs[scope].components:
        return catalogs[scope].components[identifier]
    return None


def parse_json(json_string: str, default: Any) -> list[str]:
    """Utility method to parse JSON strings with error handling.

    Args:
        json_string (str): The JSON string to parse.
        default (Any): The default value to use if the JSON string is invalid.

    Returns:
        list[str]: The parsed list of strings.

    Raises:
        ValueError: If the JSON string is invalid.
    """
    try:
        parsed_data = json.loads(json_string)

        if not isinstance(parsed_data, list):
            logger.warning("JSON does not contain a list, converting to list: %s", json_string)
            return _convert_to_list(parsed_data)

        result = []
        for item in parsed_data:
            if not isinstance(item, str):
                result.append(str(item))
            else:
                result.append(item)

        return result
    except json.JSONDecodeError as exception:
        if default is not None:
            return _convert_to_list(default)
        logger.error(
            "[pipeline_helper] An error occurred while parsing the JSON string: %s - %s", json_string, str(exception)
        )
        raise ValueError("Invalid JSON format.") from exception


def _convert_to_list(value: Any) -> list[str]:
    """Convert the value to a list of strings.

    Args:
        value (Any): The value to convert.

    Returns:
        list[str]: The converted list of strings.

    Raises:
        ValueError: If the value is not a list or a string.
    """
    if isinstance(value, list):
        return [str(item) for item in value]
    elif isinstance(value, str):
        return [value]
    return [str(value)]
