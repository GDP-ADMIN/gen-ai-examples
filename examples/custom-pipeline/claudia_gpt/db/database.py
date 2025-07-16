"""Database abstraction module for managing data storage operations.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class Table(Enum):
    """Enumeration of database table names.

    Attributes:
        ABBREVIATIONS (str): Table name for storing abbreviations
        CATEGORIES (str): Table name for storing categories.
        AGENTS (str): Table name for storing agents.
        AGENTS_ROLES (str): Table name for storing relationship between agents and roles.
        AGENT_EXAMPLE_QUESTIONS (str): Table name for storing agent example questions.
        AGENT_EXAMPLE_QUESTIONS_REQUIRED_MODULES (str): Table name for storing required modules for example questions.
        SETTINGS (str): Table name for storing settings.
        URL_MAPPINGS (str): Table name for storing url mappings.
        RATE_LIMITS (str): Table name for storing rate limit configurations.
        PROMPT_TEMPLATES (str): Table name for storing prompt templates.
        TOPIC_SCHEMAS (str): Table name for storing topic and schema configurations.
    """

    ABBREVIATIONS = "abbreviations"
    CATEGORIES = "categories"
    AGENTS = "agents"
    AGENTS_ROLES = "agents_roles"
    AGENT_EXAMPLE_QUESTIONS = "agent_example_questions"
    AGENT_EXAMPLE_QUESTIONS_REQUIRED_MODULES = "agent_example_questions_required_modules"
    SETTINGS = "settings"
    URL_MAPPINGS = "url_mappings"
    RATE_LIMITS = "rate_limits"
    PROMPT_TEMPLATES = "prompt_templates"
    TOPIC_SCHEMAS = "topic_schemas"


class BaseDatabase(ABC):
    """Base class defining the interface for database operations.

    This class provides an abstraction layer over different database technologies, allowing for
    consistent interaction with databases regardless of the underlying system.
    """

    @abstractmethod
    def insert(self, table: str, data: dict[str, Any]) -> str:
        """Insert a new record into the specified table.

        Args:
            table (str): The name of the table to insert the record into.
            data (dict[str, Any]): The data to insert, represented as a dictionary.

        Returns:
            str: The id of the insert operation.
        """

    @abstractmethod
    def update_one(self, table: str, query: dict[str, Any], update_data: dict[str, Any]) -> str:
        """Update a single record in the specified table that matches the given query criteria.

        Args:
            table (str): The name of the table to update.
            query (dict[str, Any]): The criteria used to select the record to update.
            update_data (dict[str, Any]): The data to update in the selected record.

        Returns:
            str: The id of the update operation.
        """

    @abstractmethod
    def find_all(self, table: str, query: dict[str, Any]) -> list[dict[str, Any]]:
        """Find all records in the specified table that match the given query criteria.

        Args:
            table (str): The name of the table to query.
            query (dict[str, Any]): The criteria used to select records.

        Returns:
            list[dict[str, Any]]: A list of dictionaries, each representing a record that matches the query.
        """

    @abstractmethod
    def find_one(self, table: str, query: dict[str, Any]) -> dict[str, Any] | None:
        """Find a single record in the specified table that matches the given query criteria.

        Args:
            table (str): The name of the table to query.
            query (dict[str, Any]): The criteria used to select the record.

        Returns:
            dict[str, Any] | None: A dictionary representing the found record, or None if no match was found.
        """
