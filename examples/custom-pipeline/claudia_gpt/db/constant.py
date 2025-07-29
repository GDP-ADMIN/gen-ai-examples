"""This module defines constants for database types used in the application.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from enum import StrEnum


class DatabaseType(StrEnum):
    """Enumeration of database type.

    Attributes:
        MARIADB (str): MariaDB database type.
        POSTREGSQL (str): PostgreSQL database type.
    """

    MARIADB = "mariadb"
    POSTREGSQL = "postgresql"
