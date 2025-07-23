FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Create working directory
WORKDIR /app

# Clone multi-mcp repository
RUN git clone https://github.com/samuellusandi/multi-mcp.git .

# Install multi-mcp dependencies
RUN uv sync

# Clone arxiv-mcp-server fixed
RUN git clone https://github.com/RavindraGDP/arxiv-mcp-server.git

# Change directory to arxiv-mcp-server
WORKDIR /app/arxiv-mcp-server

# Install arxiv-mcp-server dependencies
RUN uv sync

# Change directory back to root
WORKDIR /app

# Add uv tools to PATH
ENV PATH="/root/.local/bin:$PATH"

# Create directories for configuration and storage
RUN mkdir -p /app/config /app/storage/papers

# Create the MCP configuration file using RUN command
RUN echo '{\
  "mcpServers": {\
    "arxiv": {\
      "command": "uv",\
      "args": [\
        "--directory",\
        "./arxiv-mcp-server",\
        "--isolated",\
        "run",\
        "arxiv-mcp-server",\
        "--storage-path", "/app/storage/papers"\
      ]\
    }\
  }\
}' > /app/config/mcp.json

# Set environment variables for arxiv-mcp-server
ENV ARXIV_STORAGE_PATH=/app/storage/papers

# Expose the SSE port
EXPOSE 8006

# Run the multi-mcp proxy directly
CMD ["uv", "run", "main.py", "--transport", "sse", "--host", "0.0.0.0", "--port", "8006", "--config", "/app/config/mcp.json"]