"""Simple Agentic Pipeline Configuration with MCP call.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import os
from enum import StrEnum

from dotenv import load_dotenv
from typing import Any, TypedDict

from .preset_config import McpPresetConfig
# from .response_synthesizer import McpResponseSynthesizer

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin
# from gllm_core.event import EventEmitter

# Imports for RS
from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.constants import EventLevel, EventType
from gllm_inference.schema import PromptRole as PromptRole
from gllm_generation.response_synthesizer.response_synthesizer import BaseResponseSynthesizer

from gllm_agents.agent import Agent
from gllm_agents.mcp.client import MCPClient
from langchain_openai import ChatOpenAI

from .mcp_config import get_mcp_servers

load_dotenv(override=True)

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


class McpResponseSynthesizer(BaseResponseSynthesizer):

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
        print("Initiating MCP Servers...")
        print(zapier_url)
        async with MCPClient(get_mcp_servers(zapier_url)) as mcp:
            tools = mcp.get_tools()
            print("Tools: ", tools)

            llm = ChatOpenAI(model="gpt-4.1")
            agent = Agent(
                name="HelloAgent",
                instruction="You are a helpful assistant that can utilize all tools given to you to solve the user's input.",
                llm=llm,
                tools=tools,
                verbose=True
            )

            response = await agent.arun(query)

            if event_emitter:
                await event_emitter.emit(response['output'], event_level=EventLevel.INFO, event_type=EventType.RESPONSE)
            return response['output']


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
        response_synthesizer_step = step(
            component=McpResponseSynthesizer(),
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
