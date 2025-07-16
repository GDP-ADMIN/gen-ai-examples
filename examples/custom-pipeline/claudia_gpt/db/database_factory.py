"""Provides a factory for creating database instances based on configuration.

This module contains the `DatabaseFactory` class, which is responsible for creating instances of
different database implementations based on the configured database type. It supports SQL databases
and dynamically selects the appropriate provider based on the specified database
type in the environment variables.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from claudia_gpt.config.constant import DATABASE_TYPE
from claudia_gpt.db.constant import DatabaseType
from claudia_gpt.db.database import BaseDatabase
from claudia_gpt.db.service.agent_example_question_service import (
    BaseAgentExampleQuestionService,
    SQLAgentExampleQuestionService,
)
from claudia_gpt.db.service.agent_service import BaseAgentService, SQLAgentService
from claudia_gpt.db.service.setting_service import BaseSettingService, SQLSettingService
from claudia_gpt.db.sql_database import SQLDatabase


class DatabaseFactory:
    """A factory for creating instances of different database implementations.

    This class provides a method `get_database()` for retrieving a database instance based on the
    configured database type. It supports SQL databases and dynamically selects
    the appropriate provider based on the specified database type in the environment variables.
    """

    _instance = None
    _agent_service_instance = None
    _agent_example_question_service_instance = None
    _setting_service_instance = None

    @classmethod
    def get_database(cls) -> BaseDatabase:
        """Retrieve an instance of the configured database.

        Returns:
            BaseDatabase: An instance of the configured database implementation.

        Raises:
            ValueError: If the configured database type is unknown.
        """
        if cls._instance is None:
            provider_map = {DatabaseType.MARIADB.value: SQLDatabase, DatabaseType.POSTREGSQL.value: SQLDatabase}
            provider_class = provider_map.get(DATABASE_TYPE)
            if provider_class:
                cls._instance = provider_class()
            else:
                raise ValueError(f"Unknown database type: {DATABASE_TYPE}")

        return cls._instance

    @classmethod
    def get_agent_service(cls) -> BaseAgentService:
        """Retrieve an instance of the agent service.

        Returns:
            BaseAgentService: An instance of the configured agent service implementation.

        Raises:
            ValueError: If the database instance is unknown.
        """
        if cls._agent_service_instance is None:
            database = cls.get_database()
            provider_map = {
                DatabaseType.MARIADB.value: SQLAgentService,
                DatabaseType.POSTREGSQL.value: SQLAgentService,
            }
            provider_class = provider_map.get(DATABASE_TYPE)
            cls._agent_service_instance = provider_class(database)

        return cls._agent_service_instance

    @classmethod
    def get_agent_example_question_service(cls) -> BaseAgentExampleQuestionService:
        """Retrieve an instance of the agent example question service.

        Returns:
            BaseAgentExampleQuestionService: An instance of the configured
                agent example question service implementation.

        Raises:
            ValueError: If the database instance is unknown.
        """
        if cls._agent_example_question_service_instance is None:
            database = cls.get_database()
            provider_map = {
                DatabaseType.MARIADB.value: SQLAgentExampleQuestionService,
                DatabaseType.POSTREGSQL.value: SQLAgentExampleQuestionService,
            }
            provider_class = provider_map.get(DATABASE_TYPE)
            cls._agent_example_question_service_instance = provider_class(database)

        return cls._agent_example_question_service_instance

    @classmethod
    def get_setting_service(cls) -> BaseSettingService:
        """Retrieve an instance of the setting service.

        Returns:
            BaseSettingService: An instance of the configured setting service implementation.
        """
        if cls._setting_service_instance is None:
            database = cls.get_database()
            provider_map = {
                DatabaseType.MARIADB.value: SQLSettingService,
                DatabaseType.POSTREGSQL.value: SQLSettingService,
            }
            provider_class = provider_map.get(DATABASE_TYPE)
            cls._setting_service_instance = provider_class(database)

        return cls._setting_service_instance


def get_agent_service() -> BaseAgentService:
    """Dependency function to get the BaseAgentService instance.

    Returns:
        BaseAgentService: A singleton instance of the agent service.
    """
    return DatabaseFactory.get_agent_service()


def get_agent_example_question_service() -> BaseAgentExampleQuestionService:
    """Dependency function to get the BaseAgentExampleQuestionService instance.

    Returns:
        BaseAgentExampleQuestionService: A singleton instance of the agent example question service.
    """
    return DatabaseFactory.get_agent_example_question_service()


def get_setting_service() -> BaseSettingService:
    """Dependency function to get the BaseSettingService instance.

    Returns:
        BaseSettingService: A singleton instance of the setting service.
    """
    return DatabaseFactory.get_setting_service()
