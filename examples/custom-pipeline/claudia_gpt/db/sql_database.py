"""Implements the base database class using SQL.

This module provides a concrete implementation of the base database class, utilizing SQLAlchemy for
interacting with a SQL database. It supports basic operations such as insert, update, and query, allowing
for the manipulation and retrieval of data within a SQL database context.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)

References:
    [1] https://docs.sqlalchemy.org/en/20/core/pooling.html#disconnect-handling-pessimistic
"""

from typing import Any, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from claudia_gpt.config.constant import GLCHAT_DB_URL
from claudia_gpt.db.database import BaseDatabase, Table
from claudia_gpt.db.sql_model import (
    Abbreviation,
    Agent,
    AgentRole,
    PromptTemplate,
    RateLimit,
    TopicSchema,
    UrlMapping,
)
from claudia_gpt.utils.logger import logger

Base = declarative_base()


class SQLDatabase(BaseDatabase):
    """A SQL-based implementation of the base database class.

    Utilizes SQLAlchemy for database interactions, providing methods for inserting, updating,
    and querying records within a SQL database. Supports dynamic table/model mapping to facilitate
    operations across different database tables.

    Attributes:
        engine (Engine): SQL database engine.
        Session (Session): SQL scoped session.
        model_mappings (dict[str, str]): SQL model mappings.
    """

    def __init__(self, pool_size: int = 50, max_overflow: int = 50):
        """Initialize a new instance of SQLDatabase, establishing a connection to the SQL server.

        Args:
            pool_size (int): The number of connections to keep in the pool. Defaults to 50.
            max_overflow (int): The number of connections to allow in excess of the pool_size. Defaults to 50.
        """
        self.engine = create_engine(
            GLCHAT_DB_URL,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))

        self.model_mappings = {
            Table.ABBREVIATIONS.value: Abbreviation,
            Table.AGENTS.value: Agent,
            Table.AGENTS_ROLES.value: AgentRole,
            Table.URL_MAPPINGS.value: UrlMapping,
            Table.RATE_LIMITS.value: RateLimit,
            Table.PROMPT_TEMPLATES.value: PromptTemplate,
            Table.TOPIC_SCHEMAS.value: TopicSchema,
        }

    def insert(self, table: str, data: dict[str, Any]) -> str:
        """Insert a new record into the specified table.

        Args:
            table (str): The name of the table to insert the record into.
            data (dict[str, Any]): The data to insert, represented as a dictionary.

        Returns:
            str: The id of the insert operation.
        """
        session = self.Session()
        try:
            model = self._get_model(table)
            obj = model(**data)
            session.add(obj)
            session.commit()
            return obj.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_one(self, table: str, query: dict[str, Any], update_data: dict[str, Any]) -> str:
        """Update a single record in the specified table that matches the given query criteria.

        Args:
            table (str): The name of the table to update.
            query (dict[str, Any]): The criteria used to select the record to update.
            update_data (dict[str, Any]): The data to update in the selected record.

        Returns:
            str: The id of the update operation.
        """
        session = self.Session()
        try:
            model = self._get_model(table)
            obj = session.query(model).filter_by(**query).first()
            if obj:
                for key, value in update_data.items():
                    setattr(obj, key, value)
                session.commit()
                return obj.id
            else:
                raise ValueError("Object not found.")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def find_all(self, table: str, query: dict[str, Any]) -> list[dict[str, Any]]:
        """Find all records in the specified table that match the given query criteria.

        Args:
            table (str): The name of the table to query.
            query (dict[str, Any]): The criteria used to select records.

        Returns:
            list[dict[str, Any]]: A list of dictionaries, each representing a record that matches the query.
        """
        session = self.Session()
        try:
            model = self._get_model(table)
            result = session.query(model).filter_by(**query).all()
            return [row.__dict__ for row in result]
        finally:
            session.close()

    def find_one(self, table: str, query: dict[str, Any]) -> dict[str, Any] | None:
        """Find a single record in the specified table that matches the given query criteria.

        Args:
            table (str): The name of the table to query.
            query (dict[str, Any]): The criteria used to select the record.

        Returns:
            dict[str, Any] | None: A dictionary representing the found record, or None if no match was found.
        """
        session = self.Session()
        try:
            model = self._get_model(table)
            if model:
                result = session.query(model).filter_by(**query).first()
                if result:
                    return {column.name: getattr(result, column.name) for column in result.__table__.columns}
        except Exception as e:
            logger.info(f"Error finding record: {e}")
            return None
        finally:
            session.close()

    def _get_model(self, table: str) -> Type[Base]:
        """Retrieve the SQLAlchemy model class associated with the specified table name.

        Args:
            table (str): The name of the table (or model mapping key).

        Returns:
            Type[Base]: The SQLAlchemy model class associated with the specified table.

        Raises:
            ValueError: If no model is found for the specified table.
        """
        model = self.model_mappings.get(table)
        if model is None:
            raise ValueError(f"No model found for table '{table}'.")
        return model
