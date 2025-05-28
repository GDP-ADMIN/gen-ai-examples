FROM python:3.12-slim

WORKDIR /app

# Copy and install Python dependencies (including uv)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install arxiv-mcp-server using uv
RUN uv tool install arxiv-mcp-server

# Create storage directory
RUN mkdir -p /app/papers

EXPOSE 8006

# Set environment variables for paper storage
ENV ARXIV_STORAGE_PATH=/app/papers

CMD ["mcp-proxy", "--sse-port=8006", "--sse-host=0.0.0.0", "--", "uv", "tool", "run", "arxiv-mcp-server", "--storage-path", "/app/papers"]