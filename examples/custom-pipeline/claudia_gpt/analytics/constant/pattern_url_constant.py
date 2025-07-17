"""Module with constants for URL patterns.

Authors:
    Immanuel Rhesa (immanuel.rhesa@gdplabs.id)
"""

PLOT_URL_PATTERN = (
    r"https://catapa\.com/plot/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
DATA_URL_PATTERN = (
    r"https://catapa\.com/data/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
