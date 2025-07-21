"""Module containing SQLAlchemy models for the application database.

Authors:
    Berty C L Tobing <berty.c.l.tobing@gdplabs.id>
"""

import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, relationship

from claudia_gpt.db.database import Table

Base = declarative_base()


class Abbreviation(Base):
    """Represents a record of abbreviations.

    Attributes:
        id (str): Unique identifier of the rate limit record.
        agent_id (str): Agent id.
        abbreviation (str): Abbreviation.
        expansion (str): Expansion of the abbreviation.
        agent (Agent): The associated agent.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.ABBREVIATIONS.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String(36), ForeignKey(f"{Table.AGENTS.value}.id"), nullable=False)
    abbreviation = Column(String(255), nullable=False)
    expansion = Column(Text, nullable=False)

    # relationships
    agent: Mapped["Agent"] = relationship("Agent", back_populates="abbreviations")


class Category(Base):
    """Represents a record of categories.

    Attributes:
        id (str): Unique identifier of the mapping.
        name (str): Category name.
        agent_example_questions (list[AgentExampleQuestion]): List of associated agent example questions.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.CATEGORIES.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, unique=True)

    # relationships
    agent_example_questions: Mapped[list["AgentExampleQuestion"]] = relationship(
        "AgentExampleQuestion", back_populates="category"
    )


class AgentRole(Base):
    """Represents an agent role entity in the system.

    Attributes:
        id (str): Unique identifier for the agent.
        agent_id (str): The agent id.
        role_id (str): The role id.
        tenant (str): The tenant.
        agent (Agent): The associated agent.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.AGENTS_ROLES.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String(36), ForeignKey(f"{Table.AGENTS.value}.id"), nullable=False)
    role_id = Column(String(36), nullable=False)
    tenant = Column(String(255), nullable=False)

    # relationships
    agent: Mapped["Agent"] = relationship("Agent", back_populates="agent_roles")


class Agent(Base):
    """Represents an agent entity in the system.

    Attributes:
        id (str): Unique identifier for the agent.
        name (str): Name of the agent.
        type (str): Type of the agent.
        public (bool): Flag whether agent is public or not.
        description (str): Description of the agent.
        svg_icon (str): SVG icon of the agent.
        abbreviations (list[Abbreviation]): List of associated abbreviations.
        agent_roles (list[AgentRole]): List of associated agent roles.
        agent_example_questions (list[AgentExampleQuestion]): List of associated agent example questions.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.AGENTS.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(255), nullable=False)
    public = Column(Boolean, nullable=False)
    description = Column(Text, nullable=False)
    svg_icon = Column(Text, nullable=False)

    # relationships
    abbreviations: Mapped[list["Abbreviation"]] = relationship("Abbreviation", back_populates="agent")
    agent_roles: Mapped[list["AgentRole"]] = relationship("AgentRole", back_populates="agent")
    agent_example_questions: Mapped[list["AgentExampleQuestion"]] = relationship(
        "AgentExampleQuestion", back_populates="agent"
    )


class AgentExampleQuestion(Base):
    """Represents a record of agent example questions.

    Attributes:
        id (str): Unique identifier of the mapping.
        agent_id (str): The agent id.
        category_id (str | None): The category id.
        question_header (str): Example question header.
        question (str): Example question.
        agent (Agent): The associated agent.
        category (Category | None): The associated category.
        required_active_modules (list[AgentExampleQuestionRequiredModule]): List of required active modules.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.AGENT_EXAMPLE_QUESTIONS.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String(36), ForeignKey(f"{Table.AGENTS.value}.id"), nullable=False)
    category_id = Column(String(36), ForeignKey(f"{Table.CATEGORIES.value}.id"), nullable=True)
    question_header = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)

    # relationships
    agent: Mapped["Agent"] = relationship("Agent", back_populates="agent_example_questions")
    category: Mapped["Category"] = relationship("Category", back_populates="agent_example_questions")
    required_active_modules: Mapped[list["AgentExampleQuestionRequiredModule"]] = relationship(
        "AgentExampleQuestionRequiredModule", back_populates="agent_example_question"
    )


class AgentExampleQuestionRequiredModule(Base):
    """Represents a required module for an agent example question.

    Attributes:
        agent_example_question_id (str): The agent example question id.
        name (str): Name of the required module.
        agent_example_question (AgentExampleQuestion): The associated agent example question.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.AGENT_EXAMPLE_QUESTIONS_REQUIRED_MODULES.value
    agent_example_question_id = Column(String(36), ForeignKey("agent_example_questions.id"), primary_key=True)
    name = Column(String(255), primary_key=True, nullable=False)

    # relationships
    agent_example_question = relationship("AgentExampleQuestion", back_populates="required_active_modules")


class Setting(Base):
    """Represents a record of settings.

    Attributes:
        id (str): Unique identifier of the setting.
        setting_key (str): Setting key.
        setting_value (str): Setting value.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.SETTINGS.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    setting_key = Column(String(255), nullable=False, unique=True)
    setting_value = Column(Text, nullable=False)


class UrlMapping(Base):
    """Represents a mapping between a URL and its valid counterpart.

    Attributes:
        id (str): Unique identifier of the mapping.
        url (str): The validated and possibly transformed URL.
        tenant (str): The tenant associated with the URL.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.URL_MAPPINGS.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(Text, nullable=False)
    tenant = Column(String(255), nullable=False)


class RateLimit(Base):
    """Represents a record of rate limit for a particular tenant.

    Attributes:
        id (str): Unique identifier of the rate limit record.
        tenant (str): Identifier for the tenant.
        rate_limit (str): Rate limit configuration for a particular tenant.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.RATE_LIMITS.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant = Column(String(255), nullable=False, unique=True)
    rate_limit = Column(String(255), nullable=False)


class PromptTemplate(Base):
    """Represents a record of prompt templates.

    Attributes:
        id (str): Unique identifier of the prompt template record.
        name (str): Identifier for the prompt template name.
        system_prompt (str): System prompt template.
        user_prompt (str): User prompt template.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.PROMPT_TEMPLATES.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, unique=True)
    system_prompt = Column(Text, nullable=False)
    user_prompt = Column(Text)


class TopicSchema(Base):
    """Represents a record of schema for a particular topic.

    Attributes:
        id (str): Unique identifier of the schema record.
        module (str): Module for the schema.
        topic (str): Topic for the schema.
        schema_text (str): Schema database to be stored.
        required_active_module (str): Required active module for the schema.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = Table.TOPIC_SCHEMAS.value
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    module = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False)
    schema_text = Column(Text, nullable=False)
    required_active_module = Column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint("module", "topic", name="UK_TOPICSCHEMAS_MODULE_TOPIC"),)
