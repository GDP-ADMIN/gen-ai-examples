"""DB Adapter Class using SQLAlchemy.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)

References:
    [1] https://docs.sqlalchemy.org/en/20/core/pooling.html#disconnect-handling-pessimistic
"""

from typing import Union

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.engine import Engine


class DatabaseAdapter:
    """Initializes a database engine and session using SQLAlchemy.

    Provides a scoped session and a base query property for interacting with the database.
    """

    engine = None
    db = None
    base = orm.declarative_base()

    @classmethod
    def initialize(  # pylint: disable=too-many-positional-arguments
        cls,
        engine_or_url: Union[Engine, str],
        pool_size: int = 50,
        max_overflow: int = 0,
        autocommit: bool = False,
        autoflush: bool = True,
    ):
        """Creates a new database engine and session.

        Must provide either an engine or a database URL.

        Args:
            engine_or_url (Engine|str): Sqlalchemy engine object or database URL.
            pool_size (int): The size of the database connections to be maintained. Default is 50.
            max_overflow (int): The maximum overflow size of the pool. Default is 0.
            autocommit (bool): If True, all changes to the database are committed immediately. Default is False.
            autoflush (bool): If True, all changes to the database are flushed immediately. Default is True.
        """
        if isinstance(engine_or_url, str):
            cls.engine = sqlalchemy.create_engine(
                engine_or_url,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_pre_ping=True,  # Claudia adjustment: to avoid db disconnecting
            )
        else:
            cls.engine = engine_or_url

        session_local = orm.sessionmaker(autocommit=autocommit, autoflush=autoflush, bind=cls.engine)
        cls.db = orm.scoped_session(session_local)
        cls.base.query = cls.db.query_property()

    @classmethod
    def has_table(cls, table_name: str):
        """Check if a table exists in the database.

        Args:
            table_name (str): Table name to check.

        Returns:
            bool: True if table exists in the database.
        """
        inspector = sqlalchemy.inspect(cls.engine)
        if inspector:
            return inspector.has_table(table_name)
        return False
