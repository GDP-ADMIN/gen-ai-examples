"""Simple Agentic Pipeline Configuration with MCP call.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import os
from dotenv import load_dotenv
from typing import Any

from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin

from mcp_pipeline.components.chat_history_manager import McpChatHistoryManager
from mcp_pipeline.components.response_synthesizer import McpResponseSynthesizer
from mcp_pipeline.preset_config import McpPresetConfig
from mcp_pipeline.state import McpState, McpStateKeys


load_dotenv(override=True)


class McpPipelineBuilderPlugin(PipelineBuilderPlugin):
    """MCP Pipeline Builder Plugin.

    This pipeline will attempt to pass the user query to the response synthesizer,
    but utilizing tools that are provided by MCP Servers if needed.

    Inherits attributes from `PipelineBuilderPlugin`.
    """

    name = "mcp-pipeline"
    preset_config_class = McpPresetConfig

    def __init__(self):
        """Initialize the MCP pipeline builder."""
        super().__init__()
        self.data_store = SQLAlchemySQLDataStore(engine_or_url=os.getenv("GLCHAT_DB_URL"))

    async def build(self, pipeline_config: dict[str, Any]) -> Pipeline:
        """Build the pipeline.

        Args:
            pipeline_config (dict[str, Any]): The pipeline configuration.

        Returns:
            Pipeline: The simple pipeline.
        """
        model = str(pipeline_config["model_name"]) if "model_name" in pipeline_config else os.getenv("LANGUAGE_MODEL", "openai/gpt-4.1")
        key = os.getenv(pipeline_config["api_key"]) if "api_key" in pipeline_config else os.getenv("LLM_API_KEY", "")
        
        mcp_server_url_key = pipeline_config.get("mcp_server_url") or "MCP_SERVER_URL"
        mcp_server_url = os.getenv(mcp_server_url_key, "")

        response_synthesizer_step = step(
            component=McpResponseSynthesizer(model=model, key=key, mcp_server_url=mcp_server_url),
            input_state_map={
                McpStateKeys.QUERY: McpStateKeys.QUERY,
                McpStateKeys.EVENT_EMITTER: McpStateKeys.EVENT_EMITTER,
            },
            output_state=McpStateKeys.RESPONSE,
        )

        save_message_step = step(
            component=McpChatHistoryManager(data_store=self.data_store),
            input_state_map={
                McpStateKeys.QUERY: McpStateKeys.QUERY,
                McpStateKeys.RESPONSE: McpStateKeys.RESPONSE,
                McpStateKeys.EVENT_EMITTER: McpStateKeys.EVENT_EMITTER,
            },
            output_state=McpStateKeys.HISTORY,
            runtime_config_map = {
                "user_id": "user_id",
                "conversation_id": "conversation_id",
                "parent_id": "parent_id",
                "user_message_id": "user_message_id",
                "assistant_message_id": "assistant_message_id",
                "source": "source",
                "quote": "quote",
                "attachments": "attachments",
                "original_message": "original_message",
            },
            fixed_args={"operation": "write"},
        )

        return Pipeline(
            steps=[response_synthesizer_step, save_message_step],
            state_type=McpState
        )

    def build_initial_state(
        self, request: dict[str, Any], pipeline_config: dict[str, Any], **kwargs: Any
    ) -> McpState:
        """Build the initial state for pipeline invoke.

        Args:
            request (dict[str, Any]): The given request from the user.
            pipeline_config (dict[str, Any]): The pipeline configuration.
            **kwargs (Any): A dictionary of arguments required for building the initial state.

        Returns:
            McpState: The initial state.
        """
        return McpState(
            query=request.get("message"),
            response=None,
            history=None,
            event_emitter=kwargs.get("event_emitter")
        )
