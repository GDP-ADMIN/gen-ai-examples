"""Defines a weather tool that can be used to get the weather for a specified city.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from gllm_agents.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)

# Combined weather data storage with detailed information
WEATHER_DATA = {
    "Jakarta": {"temperature": "32°C", "conditions": "Partly cloudy with high humidity", "humidity": "78%"},
    "Singapore": {"temperature": "30°C", "conditions": "Scattered thunderstorms", "humidity": "85%"},
    "Tokyo": {"temperature": "25°C", "conditions": "Clear skies", "humidity": "65%"},
    "London": {"temperature": "18°C", "conditions": "Light rain", "humidity": "82%"},
    "New York": {"temperature": "22°C", "conditions": "Sunny", "humidity": "60%"},
    "Sydney": {"temperature": "24°C", "conditions": "Clear", "humidity": "70%"},
}


def weather_tool(city: str) -> str:
    """Gets the weather for a specified city.

    Args:
        city: The name of the city to get weather for.

    Returns:
        A string describing the weather conditions.
    """
    city_name = city.strip().title()

    weather = WEATHER_DATA.get(city_name)
    if weather:
        logger.info(f"Found weather for {city_name}: {weather}")
        return weather
    else:
        message = f"Weather data not available for {city}"
        logger.warning(message)
        return message
