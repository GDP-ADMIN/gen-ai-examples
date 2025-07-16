"""This module defines services for interacting with agent example question data in different types of databases.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from abc import ABC, abstractmethod
from typing import Any

from claudia_gpt.db.sql_database import SQLDatabase
from claudia_gpt.db.sql_model import AgentExampleQuestion
from claudia_gpt.utils.logger import logger


class BaseAgentExampleQuestionService(ABC):
    """An abstract of the BaseAgentExampleQuestionService."""

    @abstractmethod
    def find_example_questions(
        self,
        agent_id: str,
        agent_ids: list[str],
        category_id: str | None = None,
        active_modules: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Find and retrieves all agent example questions.

        Args:
            agent_id (str): The agent id of the agent example question.
            agent_ids (list[str]): The valid agent ids.
            category_id (str | None): The category ID of the question example. Defaults to None.
            active_modules (list[str] | None): The list of active modules. Defaults to None.

        Returns:
            list[dict[str, Any]]: A dictionary containing list of question examples.
        """


class SQLAgentExampleQuestionService(BaseAgentExampleQuestionService):
    """A concrete implementation of the BaseAgentExampleQuestionService for SQL database.

    Attributes:
        _database (SQLDatabase): The SQL database.
    """

    def __init__(self, database: SQLDatabase) -> None:
        """Initialize a new instance of SQLAgentExampleQuestionService.

        Args:
            database (SQLDatabase): The SQL database.
        """
        self._database = database

    def find_example_questions(
        self,
        agent_id: str,
        agent_ids: list[str],
        category_id: str | None = None,
        active_modules: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Find and retrieves all agent example questions.

        Args:
            agent_id (str): The agent id of the agent example question.
            agent_ids (list[str]): The valid agent ids.
            category_id (str | None): The category ID to filter question examples. Defaults to None.
            active_modules (list[str] | None): The list of active modules. Defaults to None.

        Returns:
            list[dict[str, Any]]: A dictionary containing the example's id, question, question header, and agent type.
        """
        with self._database.Session() as session:
            try:
                query = session.query(AgentExampleQuestion)
                query = query.filter(AgentExampleQuestion.agent_id == agent_id)
                query = query.filter(AgentExampleQuestion.agent_id.in_(agent_ids))

                if category_id:
                    query = query.filter(AgentExampleQuestion.category_id == category_id)

                examples = query.all()

                if active_modules is not None:
                    filtered_examples = []
                    for example in examples:
                        required_modules = [module.name for module in example.required_active_modules]
                        if not required_modules or all(module in active_modules for module in required_modules):
                            filtered_examples.append(example)
                else:
                    filtered_examples = examples

                examples_list = [
                    {
                        "id": example.id,
                        "question": example.question,
                        "question_header": example.question_header,
                        "category": example.category,
                    }
                    for example in filtered_examples
                ]
                return examples_list
            except Exception as e:
                session.rollback()
                logger.error(f"Error finding examples: {e}")
                raise e
