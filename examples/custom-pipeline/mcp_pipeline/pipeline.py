"""Simple Agentic Pipeline Configuration with MCP call.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import os
from enum import StrEnum

from dotenv import load_dotenv
from typing import Any, TypedDict

from mcp_pipeline.preset_config import McpPresetConfig

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
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


# TODO debug why this cannot be in a separate file without failing to import.
class McpResponseSynthesizer(BaseResponseSynthesizer):

    def __init__(self, model: str, key: str):
        super().__init__()
        self.model = model
        self.key = key

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
        zapier_url = os.getenv("ZAPIER_SERVER_URL", "")
        client = MultiServerMCPClient(get_mcp_servers(zapier_url))
        tools = await client.get_tools()

        model = self.model
        key = self.key

        agent = create_react_agent(
            name="HelloAgent",
            prompt="You are a helpful assistant that can utilize all tools given to you to solve the user's input.",
            model=get_language_model(model, key),
            tools=tools,
        )

        final_response = ""
        processed_tool_ids = set()

        async for chunk in agent.astream({"messages": query}, stream_mode="values"):
            if isinstance(chunk, dict) and 'messages' in chunk:
                messages = chunk['messages']

                for message in messages:
                    if hasattr(message, 'additional_kwargs') and 'tool_calls' in message.additional_kwargs:
                        tool_calls = message.additional_kwargs['tool_calls']
                        for tool_call in tool_calls:
                            if tool_call['id'] not in processed_tool_ids:
                                processed_tool_ids.add(tool_call['id'])
                                
                                tool_info = f"Called tool `{tool_call['function']['name']}` with arguments: {tool_call['function']['arguments']}"
                                print(tool_info)

                                if event_emitter:
                                    await event_emitter.emit(
                                        tool_info,
                                        event_level=EventLevel.INFO, 
                                        event_type=EventType.DATA
                                    )

        if 'messages' in chunk:
            messages = chunk['messages']
            last_ai_message = next((msg for msg in reversed(messages) 
                                   if hasattr(msg, 'content') and msg.content), None)
            final_response = last_ai_message.content if last_ai_message else "No response generated"

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
        model = pipeline_config["model_name"] if "model_name" in pipeline_config else os.getenv("LANGUAGE_MODEL", "openai/gpt-4.1")
        key = pipeline_config["api_key"] if "api_key" in pipeline_config else os.getenv("LLM_API_KEY", "")

        response_synthesizer_step = step(
            component=McpResponseSynthesizer(model=model, key=key),
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
