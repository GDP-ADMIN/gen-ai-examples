"""Example application using GLLM Backend library."""

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi import APIRouter

# Load environment variables from .env file
load_dotenv()

# Import the GLLM Backend library
from gdplabs_gen_ai_starter_gllm_backend import create_app

# Create a custom router
custom_router = APIRouter(prefix="/custom", tags=["custom"])

@custom_router.get("/hello")
async def hello():
    return {"message": "Hello from custom router!"}

# Create the FastAPI application
app = create_app()

# Include the custom router
app.include_router(custom_router)

# Add CORS middleware if not already added
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # Run the application
    print("Running custom GLLM backend application...")
    uvicorn.run(app, port=8008)
    print("Custom GLLM backend application stopped.")
