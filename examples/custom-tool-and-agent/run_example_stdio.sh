#!/bin/bash

echo "Installing project dependencies..."
poetry install

echo "Running the example..."
poetry run python hello_agent_mcp_stdio_example.py
