"""Weather Forecast MCP Tool by SSE."""

from mcp.server.fastmcp import FastMCP
from aip_agent_quickstart.tools.weather_forecast_tool import get_weather_forecast

mcp = FastMCP("Weather_Forecast")
mcp.add_tool(get_weather_forecast)

if __name__ == "__main__":
    mcp.run(transport="sse")
