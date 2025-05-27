"""Simple Agentic Pipeline Configuration with MCP call.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import json
import uuid
import os
import time
from enum import StrEnum

from dotenv import load_dotenv
from typing import Any, TypedDict

from mcp_pipeline.preset_config import McpPresetConfig

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_plugin.pipeline.base_pipeline_preset_config import BasePipelinePresetConfig
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin

# Imports for Response Synthesizer
from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.constants import EventLevel, EventType
from gllm_inference.schema import PromptRole as PromptRole
from gllm_generation.response_synthesizer.response_synthesizer import BaseResponseSynthesizer

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseLanguageModel
from langgraph.prebuilt import create_react_agent

from mcp_pipeline.mcp_config import get_mcp_servers

load_dotenv(override=True)

def get_language_model(model: str, key: str) -> BaseLanguageModel:
    provider = model.split("/")[0]
    model_name = model.split("/")[1]
    if provider == "openai":
        return ChatOpenAI(model=model_name, api_key=key)
    else:
        raise ValueError(f"Unsupported model: {model}")


class SimpleState(TypedDict):
    """A TypedDict representing the state of the Simple Pipeline.

    Attributes:
        query (str): The user's query.
        response (str): The generated response to the user's query.
    """

    query: str
    response: str
    event_emitter: EventEmitter



class SimpleStateKeys(StrEnum):
    """List of all possible keys in SimpleState."""

    QUERY = "query"
    RESPONSE = "response"
    EVENT_EMITTER = "event_emitter"



class McpPresetConfig(BasePipelinePresetConfig):
    """A Pydantic model representing the preset config of a simple pipeline.

    Inherits attributes from `BasePipelinePresetConfig`.
    """

    mcp_server_url: str


class MaximumToolCallsException(Exception):
    """Exception raised when the maximum number of tool calls is reached."""
    pass


# TODO debug why this cannot be in a separate file without failing to import.
class McpResponseSynthesizer(BaseResponseSynthesizer):

    MAX_TOOL_CALLS = 10

    def __init__(self, model: str, key: str, mcp_server_url: str):
        super().__init__()
        self.model = model
        self.key = key
        self.mcp_server_url = mcp_server_url

    async def synthesize_response(
        self,
        query: str | None = None,
        state_variables: dict[str, Any] | None = None,
        history: list[tuple[PromptRole, str | list[Any]]] | None = None,
        event_emitter: EventEmitter | None = None,
        system_multimodal_contents: list[Any] | None = None,
        user_multimodal_contents: list[Any] | None = None
    ) -> str:
        """Synthesizes a response based on the provided query.

        This abstract method must be implemented by subclasses to define the logic for generating a response. It
        may optionally take an input `query`, some other input variables passed through `state_variables`, and an
        `event_emitter`. It returns the synthesized response as a string.

        Args:
            query (str | None, optional): The input query used to synthesize the response. Defaults to None.
            state_variables (dict[str, Any] | None, optional): Additional state variables to assist in generating the
                response. Defaults to None.
            history (list[tuple[PromptRole, str | list[Any]]] | None, optional): The chat history of the conversation
                to be considered in generating the response. Defaults to None.
            event_emitter (EventEmitter | None, optional): The event emitter for handling events during response
                synthesis. Defaults to None.
            system_multimodal_contents (list[Any] | None, optional): The system multimodal contents to be considered
                in generating the response. Defaults to None.
            user_multimodal_contents (list[Any] | None, optional): The user multimodal contents to be considered in
                generating the response. Defaults to None.

        Returns:
            str: The synthesized response.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        start_time = time.time()
        client = MultiServerMCPClient(get_mcp_servers(self.mcp_server_url))
        tools = await client.get_tools()
        for tool in tools:
            tool.name = tool.name.replace("::", "__")

        model = self.model
        key = self.key

        agent = create_react_agent(
            name="HelloAgent",
            prompt=f"""You are a helpful assistant that can utilize all tools given to you to solve the user's input.

            When there is anything related to relative time, you *must* call the get_current_time tool. Otherwise you will not be able to 
            provide an accurate response. The timezone *must* be UTC+7 Asia/Jakarta.

            Here are a few things you need to do for specific tasks:
            
            Regarding Slack:
            - Ping specific user on slack: You must first find the user's slack ID and then ping them using the format <@user_id>
            - Reminder the following when you use IDs:
                * IDs prefixed with `T` indicate Teams/Organizations (T*******)
                * IDs prefixed with `U` indicate Users (U*******)
                * IDs prefixed with `C` indicate Channels (C*******)
                * IDs prefixed with `D` indicate Direct Messages (D*******)
            - Regarding sending a message to slack channel: If a user specifies a channel, and IF the channel cannot be found, do not give up yet;
              it is likely a private channel.
                * Try sending it directly, the slack_post_message tool will throw an error if the channel truly cannot be found.
                * Remember to just use the name of the channel as ID directly!

            Regarding Github:
            - If the user does not specify a repository owner, you *must* assume it is `GDP-ADMIN`. (i.e., `bosa` becomes `GDP-ADMIN/bosa`)
            - If the user does not specify a repository owner and a repository name, you do not have to proceed; simply tell the user that you need more information.
            - Regarding issues and pull requests in github:
                * If the result is under 1000 items, you *must* use the search endpoints (i.e., search_repositories, search_issues, etc.) because
                  your query can become a lot more versatile, and the results will be much more accurate. You can filter by date, filter by user,
                  etc.
                * If the result is over 1000 items, you *must* use the list endpoints (i.e., list_repositories, list_issues, etc.) because
                  the search endpoints will not return all the results. However, do know that this endpoint doesn't have as much query capabilities,
                  i.e., there's no query, no filter by date, etc.
            """,
            model=get_language_model(model, key),
            tools=tools,
        )

        final_response = ""
        processed_tool_ids = set()

        tool_call_count = 0
        message_prefix = ""
        try:
            async for chunk in agent.astream({"messages": query}, stream_mode="values"):
                if isinstance(chunk, dict) and 'messages' in chunk:
                    messages = chunk['messages']

                    for message in messages:
                        if hasattr(message, 'additional_kwargs') and 'tool_calls' in message.additional_kwargs:
                            tool_calls = message.additional_kwargs['tool_calls']
                            for tool_call in tool_calls:
                                if tool_call['id'] not in processed_tool_ids:
                                    processed_tool_ids.add(tool_call['id'])
                                    tool_call_count += 1

                                    tool_info = f"Called tool `{tool_call['function']['name']}`"

                                    step_id = str(uuid.uuid4())
                                    tool_running_data = {
                                        "data_type": "process",
                                        "data_value": {
                                            "id": step_id,
                                            "message": tool_info,
                                            "status": "running",
                                            "time": round(time.time() - start_time, 2)
                                        },
                                    }
                                    tool_finished_data = {
                                        "data_type": "process",
                                        "data_value": {
                                            "id": step_id,
                                            "message": tool_info,
                                            "status": "finished",
                                            "time": round(time.time() - start_time, 2)
                                        },
                                    }

                                    if event_emitter:
                                        await event_emitter.emit(
                                            json.dumps(tool_running_data),
                                            event_level=EventLevel.INFO,
                                            event_type=EventType.DATA
                                        )
                                        await event_emitter.emit(
                                            json.dumps(tool_finished_data),
                                            event_level=EventLevel.INFO,
                                            event_type=EventType.DATA
                                        )
                                    
                                    if tool_call_count >= self.MAX_TOOL_CALLS:
                                        raise MaximumToolCallsException("Maximum tool calls reached")
        except MaximumToolCallsException as e:
            print(f"Error during tool calls: {e}")
            message_prefix = "We've reached the maximum number of tool calls. This is what we have so far:\n\n"
        except Exception as e:
            print(f"Error during tool calls: {e}")
            message_prefix = "An error occurred while processing your request. This is what we have so far:\n\n"

        if 'messages' in chunk:
            messages = chunk['messages']
            last_ai_message = next((msg for msg in reversed(messages) 
                                   if hasattr(msg, 'content') and msg.content), None)
            final_response = message_prefix + (last_ai_message.content if last_ai_message else "No response generated")

            if event_emitter and final_response:
                await event_emitter.emit(
                    final_response, 
                    event_level=EventLevel.INFO, 
                    event_type=EventType.RESPONSE
                )
        
        return final_response


class McpPipelineBuilderPlugin(PipelineBuilderPlugin):
    """MCP Pipeline Builder Plugin.

    This pipeline will attempt to pass the user query to the response synthesizer,
    but utilizing tools that are provided by MCP Servers if needed.

    Inherits attributes from `PipelineBuilderPlugin`.
    """

    name = "mcp-pipeline"
    preset_config_class = McpPresetConfig

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
                "query": SimpleStateKeys.QUERY,
            },
            output_state=SimpleStateKeys.RESPONSE,
        )

        return Pipeline(
            steps=[response_synthesizer_step],
            state_type=SimpleState
        )

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
