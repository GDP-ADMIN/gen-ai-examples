"""Module for handling mappings between plot URLs, data URLs, and their corresponding valid URLs.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

import re

from claudia_gpt.analytics.constant import DATA_URL_PATTERN, PLOT_URL_PATTERN
from claudia_gpt.db import Table
from claudia_gpt.db.database_factory import DatabaseFactory
from claudia_gpt.multi_tenant.context.tenant_context_holder import TenantContextHolder


def insert_url_mapping(valid_url: str) -> str:
    """Insert a mapping between the data URL and the valid data URL.

    Args:
        valid_url (str): The valid data URL.

    Returns:
        str: The insert result.
    """
    tenant = TenantContextHolder.get_tenant()
    new_document = {"url": valid_url, "tenant": tenant}

    database = DatabaseFactory.get_database()
    return database.insert(Table.URL_MAPPINGS.value, new_document)


def find_url_mapping(url: str) -> str | None:
    """Find a valid data URL based on the mapped data URL.

    Args:
        url (str): The mapped data URL.

    Returns:
        str | None: A valid data URL.
    """
    tenant = TenantContextHolder.get_tenant()
    database = DatabaseFactory.get_database()
    url_mapping_id = url.split("/")[-1]
    filter_criteria = {"id": url_mapping_id, "tenant": tenant}

    results = database.find_one(Table.URL_MAPPINGS.value, filter_criteria)

    if results:
        return results.get("url")

    return None


def replace_urls_in_string(input_string: str) -> str:
    """Replace plot URLs and data URLs in a string with their corresponding valid URLs.

    Args:
        input_string (str): The input string containing URLs to be replaced.

    Returns:
        str: The string with URLs replaced.
    """

    def replace_url(match: re.Match) -> str:
        """Replace a URL with its corresponding valid URL.

        Args:
            match (re.Match): The matched URL.

        Returns:
            str: The valid URL.
        """
        url = match.group(0)
        mapped_url = find_url_mapping(url)
        return mapped_url if mapped_url else url

    input_string = re.sub(PLOT_URL_PATTERN, replace_url, input_string)
    input_string = re.sub(DATA_URL_PATTERN, replace_url, input_string)

    return input_string
