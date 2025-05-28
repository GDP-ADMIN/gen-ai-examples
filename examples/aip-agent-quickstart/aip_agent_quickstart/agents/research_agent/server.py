"""Research Agent Server.

This module implements a FastAPI server for the Research Agent that can handle academic
and travel-related queries using MCP servers and A2A agents.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

import logging
import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import uvicorn

from a2a.server import A2AServer, ServeConfig
from gllm_agents.agent.langgraph_agent import LangGraphAgent
from research_agent.config import RESEARCH_AGENT_INSTRUCTION, SERVER_PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Research Agent",
    description="A research agent that can handle academic and travel-related queries.",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class QueryRequest(BaseModel):
    query: str
    stream: Optional[bool] = False


# Create the agent
async def create_agent() -> LangGraphAgent:
    """Create and configure the research agent.

    Returns:
        LangGraphAgent: The configured research agent
    """
    # Initialize model
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        logger.warning("OPENAI_API_KEY not found in environment variables")

    model = ChatOpenAI(
        model="gpt-4.1",
        temperature=0,
    )

    # Create the agent
    agent = LangGraphAgent(
        name="research_agent",
        instruction=RESEARCH_AGENT_INSTRUCTION,
        model=model,
        tools=[],
        verbose=True,
    )

    return agent


# Start up event
@app.on_event("startup")
async def startup_event():
    """Initialize the application resources on startup."""
    app.state.agent = await create_agent()
    logger.info("Research Agent initialized successfully")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "research_agent"}


# Process query endpoint
@app.post("/query")
async def process_query(request: QueryRequest) -> Dict[str, Any]:
    """Process a query with the research agent.

    Args:
        request: The query request containing the user's query

    Returns:
        Dict containing the agent's response
    """
    if not hasattr(app.state, "agent"):
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        if request.stream:
            # For streaming, start streaming but don't wait for completion
            # Just acknowledge the stream has started
            await app.state.agent.arun_stream(query=request.query)
            return {"result": "Streaming started", "streaming": True}
        else:
            # For non-streaming, return the full response
            response = await app.state.agent.arun(query=request.query)
            return {"result": response.get("output", ""), "streaming": False}
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# Configure A2A server
def run_a2a_server():
    """Configure and run the A2A server."""
    a2a_config = ServeConfig(
        title="Research Agent Service",
        description="A service that handles research queries for academic and travel topics",
        port=SERVER_PORT,
        llm_api_key=os.environ.get("OPENAI_API_KEY", ""),
        agent_factory=create_agent,
    )

    a2a_server = A2AServer(config=a2a_config)
    return a2a_server


# Main entrypoint
def main():
    """Start the server."""
    # Configure A2A server - we don't need to store the reference,
    # as it gets registered with app behind the scenes
    run_a2a_server()

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)


if __name__ == "__main__":
    main()
