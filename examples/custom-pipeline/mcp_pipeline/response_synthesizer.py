import os
from typing import Any

from gllm_core.event import EventEmitter as EventEmitter
from gllm_inference.schema import PromptRole as PromptRole
from gllm_generation.response_synthesizer.response_synthesizer import BaseResponseSynthesizer

from gllm_agents.agent import Agent
from gllm_rag.preset.lm import LM
from gllm_agents.mcp.client import MCPClient
from langchain_openai import ChatOpenAI

from mcp_pipeline.mcp_config import mcp_servers


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
        async with MCPClient(mcp_servers) as mcp:
            tools = mcp.get_tools()
            model_name = str(os.getenv("LANGUAGE_MODEL", ""))
            api_key = os.getenv(os.getenv("LLM_API_KEY"), "")
            # llm = LM(
            #     language_model_id=model_name,
            #     language_model_credentials=api_key,
            # )

            llm = ChatOpenAI(model="gpt-4.1")
            agent = Agent(
                name="HelloAgent",
                instruction="You are a helpful assistant that can utilize all tools given to you to solve the user's input.",
                llm=llm,
                tools=tools,
                verbose=True
            )

            response = await agent.arun(query)
            print("++++++++ RESPONSE ++++++++++")
            print(response)
            return response.__str__()
