FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_server_stdio.py .
COPY weather_forecast_tool.py .

EXPOSE 8000

CMD ["mcp-proxy", "--sse-port=8000", "--sse-host=0.0.0.0", "python", "mcp_server_stdio.py"]