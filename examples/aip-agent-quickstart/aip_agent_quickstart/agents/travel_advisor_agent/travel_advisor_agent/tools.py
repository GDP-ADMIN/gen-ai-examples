"""Tools for the TravelAdvisorAgent.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from langchain_core.tools import tool
from pydantic import BaseModel


class PlaceRecommendationsInputSchema(BaseModel):
    """Schema for place recommendations tool input."""

    city: str


@tool(args_schema=PlaceRecommendationsInputSchema)
def get_place_recommendations_tool(city: str) -> list[str]:
    """Gets a list of recommended places for the given city.

    Args:
        city: The name of the city for which to get recommendations.

    Returns:
        A list of strings, where each string is a recommended place in that city.
    """
    city_lower = city.lower()
    if city_lower == "paris":
        return [
            "Eiffel Tower",
            "Louvre Museum",
            "Notre-Dame Cathedral",
            "Arc de Triomphe",
            "Montmartre",
        ]
    elif city_lower == "jakarta":
        return [
            "Monumen Nasional",
            "Taman Fatahillah",
            "Kota Tua",
            "Kelenteng Tjoe Hwie Kiong",
        ]
    elif city_lower == "bali":
        return ["Kuta Beach", "Seminyak Beach", "Nusa Dua Beach", "Canggu Beach"]
    elif city_lower == "tokyo":
        return [
            "Tsukiji Outer Market",
            "Shibuya Crossing",
            "Senso-ji Temple",
            "Tokyo Skytree",
        ]
    else:
        return [
            f"No specific recommendations found for '{city}'. Try a different city."
        ]
