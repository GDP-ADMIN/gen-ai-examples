"""This module contains the logger for the claudia pipeline.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)
"""

from gllm_core.utils.logger_manager import LoggerManager

manager = LoggerManager()

logger = manager.get_logger()
