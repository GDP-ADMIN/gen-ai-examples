"""Provides enumerations and constants related to status.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from enum import Enum


class PlotGenerationStatus(str, Enum):
    """Enumeration of plot generation statuses.

    Attributes:
        SUCCESS (str): Plot generation success status.
        FAILED (str): Plot generation failed status.
    """

    SUCCESS = "success"
    FAILED = "failed"
