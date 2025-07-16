"""This module defines services for interacting with settings data in different types of databases.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)
"""

from abc import ABC, abstractmethod
from typing import cast

from claudia_gpt.db.sql_database import SQLDatabase
from claudia_gpt.db.sql_model import Setting
from claudia_gpt.utils.logger import logger


class BaseSettingService(ABC):
    """A base class for setting services."""

    @abstractmethod
    def get_value(self, key: str) -> str | None:
        """Get value from settings.

        Args:
            key (str): The key to search for in the settings table.

        Returns:
            str | None: The value if found, otherwise None.
        """


class SQLSettingService(BaseSettingService):
    """A concrete implementation of the BaseSettingService for SQL database.

    Attributes:
        _database (SQLDatabase): The SQL database.
    """

    def __init__(self, database: SQLDatabase):
        """Initialize a new instance of SQLSettingService.

        Args:
            database (SQLDatabase): The SQL database.
        """
        self._database = database

    def get_value(self, key: str) -> str | None:
        """Get value from settings.

        Args:
            key (str): The key to search for in the settings table.

        Returns:
            str | None: The value if found, otherwise None.
        """
        if not key:
            return None

        try:
            with self._database.Session() as session:
                result = session.query(Setting).filter(Setting.setting_key == key).one_or_none()
                return cast(str | None, result.setting_value) if result else None

        except Exception as error:
            logger.error(f"Error while getting setting value: {error}")
            return None
