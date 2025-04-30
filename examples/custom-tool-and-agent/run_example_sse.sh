#!/bin/bash

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null || true
    fi
    exit 0
}

# Set up trap to catch script termination
trap cleanup SIGINT SIGTERM EXIT

# Start the server in the background
echo "Starting the server..."
poetry run python mcp_tools/text_frequency_counter_sse.py > server.log 2>&1 &
SERVER_PID=$!

# Wait for the server to be ready
echo "Waiting for server to start..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "Server is up!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Server failed to start within 30 seconds"
        exit 1
    fi
    sleep 1
done

# Run the example
echo "Running the example..."
poetry run python hello_agent_mcp_sse_example.py

# The cleanup function will be called automatically due to the trap 
