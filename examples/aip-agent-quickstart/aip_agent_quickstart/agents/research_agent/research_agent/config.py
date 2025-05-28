"""Configuration for the Research Agent.

This module contains configuration variables and constants used by the Research Agent.
"""

# Default system prompt that instructs the agent on its capabilities and behavior
RESEARCH_AGENT_INSTRUCTION = """You are a Research Agent that helps users with academic research and travel planning.

For academic queries:
1. You can search for academic papers on arXiv
2. You can filter by keywords, authors, or topics
3. You can provide summaries and insights on research trends

For travel queries:
1. You can help users plan trips to various destinations
2. You can provide information about popular tourist spots
3. You can suggest optimal travel times and accommodations

If the user's query is not about academic research or travel planning, politely explain that
you're specialized in these two areas and cannot assist with other topics.

When answering academic queries, use the arXiv tools available to you.
For travel queries, delegate to specialized agents when available.
"""

# Port for serving the Research Agent
SERVER_PORT = 8002

# Topic classification indicators
ACADEMIC_KEYWORDS = [
    "paper",
    "research",
    "publication",
    "journal",
    "conference",
    "academic",
    "study",
    "arxiv",
    "thesis",
    "dissertation",
    "scholar",
    "professor",
    "university",
    "scientific",
    "experiment",
    "theory",
    "hypothesis",
    "findings",
    "literature review",
]

TRAVEL_KEYWORDS = [
    "travel",
    "trip",
    "vacation",
    "visit",
    "tourist",
    "tourism",
    "hotel",
    "flight",
    "accommodation",
    "destination",
    "sightseeing",
    "tour",
    "itinerary",
    "guide",
    "explore",
    "adventure",
    "journey",
    "excursion",
]
