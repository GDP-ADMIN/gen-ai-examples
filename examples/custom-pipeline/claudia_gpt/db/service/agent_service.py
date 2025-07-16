"""This module defines services for interacting with agent-related data in different types of databases.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import and_, or_

from claudia_gpt.db.sql_database import SQLDatabase
from claudia_gpt.db.sql_model import Agent, AgentRole
from claudia_gpt.multi_tenant.context.tenant_context_holder import TenantContextHolder
from claudia_gpt.utils.logger import logger


class BaseAgentService(ABC):
    """An abstract of the BaseAgentService."""

    @abstractmethod
    def find_agents(self, role_ids: list[str]) -> list[dict[str, Any]]:
        """Finds an agent by tenant and role ids.

        Args:
            role_ids (list[str]): A list of role IDs to filter agents by.

        Returns:
            list[dict[str, Any]]: A List of dictionary containing the agent's details.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.
        """
        raise NotImplementedError

    @abstractmethod
    def find_public_agents(self) -> list[dict[str, Any]]:
        """Finds public agents.

        Returns:
            list[dict[str, Any]]: A List of dictionary containing the public agent's details.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.
        """
        raise NotImplementedError

    @abstractmethod
    def find_agent(self, agent_type: str) -> dict[str, Any]:
        """Finds an agent by agent type.

        Args:
            agent_type (str): The type of the agent.

        Returns:
            dict[str, Any]: A dictionary containing the agent's details.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.
        """
        raise NotImplementedError


class SQLAgentService(BaseAgentService):
    """A concrete implementation of the AgentService for SQL database.

    Attributes:
        _database (SQLDatabase): The SQL database.
    """

    def __init__(self, database: SQLDatabase):
        """Initializes a new instance of SQLAgentService."""
        self._database = database

    def find_agents(self, role_ids: list[str]) -> list[dict[str, Any]]:
        """Concrete implementation for SQL to finds an agent by tenant and role ids.

        Args:
            role_ids (list[str]): A list of role IDs to filter agents by.

        Returns:
            list[dict[str, Any]]: A list of dictionary containing the agent's details.
        """
        tenant = TenantContextHolder.get_tenant()
        with self._database.Session() as session:
            try:
                agents = (
                    session.query(Agent)
                    .outerjoin(AgentRole)
                    .filter(
                        or_(and_(AgentRole.role_id.in_(role_ids), AgentRole.tenant == tenant), Agent.public.is_(True))
                    )
                    .distinct()
                )
                agents_list = [
                    {
                        "id": agent.id,
                        "name": agent.name,
                        "type": agent.type,
                        "description": agent.description,
                        "svg_icon": agent.svg_icon,
                        "public": agent.public,
                    }
                    for agent in agents
                ]
                return agents_list
            except Exception as e:
                session.rollback()
                logger.error(f"Error finding agents: {e}")
                raise e

    def find_public_agents(self) -> list[dict[str, Any]]:
        """Concrete implementation for SQL to find public agents by its id.

        Returns:
            list[dict[str, Any]]: A list of dictionary containing the agent's details where public is True.
        """
        with self._database.Session() as session:
            try:
                agents = session.query(Agent).filter(Agent.public.is_(True)).all()

                agents_list = [
                    {
                        "id": agent.id,
                        "name": agent.name,
                        "type": agent.type,
                        "description": agent.description,
                        "svg_icon": agent.svg_icon,
                        "public": agent.public,
                    }
                    for agent in agents
                ]

                return agents_list
            except Exception as e:
                session.rollback()
                logger.error(f"Error finding agents: {e}")
                raise e

    def find_agent(self, agent_type: str) -> dict[str, Any]:
        """Concrete implementation for SQL to find an agent by agent type.

        Args:
            agent_type (str): The type of the agent.

        Returns:
            dict[str, Any]: A dictionary containing the agent's details.

        Raises:
            Exception: If an error occurs while querying the database.
        """
        with self._database.Session() as session:
            try:
                agent = session.query(Agent).filter(Agent.type == agent_type).one()

                return {
                    "id": agent.id,
                    "name": agent.name,
                    "type": agent.type,
                    "description": agent.description,
                    "svg_icon": agent.svg_icon,
                    "public": agent.public,
                }
            except Exception as e:
                session.rollback()
                logger.error(f"Error finding agent: {e}")
                raise e
