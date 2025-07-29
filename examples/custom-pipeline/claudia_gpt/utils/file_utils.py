"""File utility functions.

Authors:
    Felicia Limanta (felicia.limanta@gdplabs.id)
"""

import os

from slugify import slugify


def sanitize_file_name(file_name: str, separator: str = "_") -> str:
    """Slugify the file name for safe content disposition header.

    Args:
        file_name (str): The original file_name to slugify.
        separator (str): The separator to use in slugify. Defaults to "_".

    Returns:
        str: The slugified file_name with preserved extension or "file"
        if the file_name is empty or only contains whitespace.

    Examples:
        "My Document.pdf" -> "my_document.pdf"
        "file with spaces & symbols!.txt" -> "file_with_spaces_symbols.txt"
    """
    file_name = file_name.strip()

    if not file_name:
        raise ValueError("File name is empty")

    name, ext = os.path.splitext(file_name)
    if not ext:
        raise ValueError(f"Unable to retrieve file extension from file {file_name}")

    slugified_name = slugify(name, separator=separator)

    if not slugified_name:
        slugified_name = "file"

    return f"{slugified_name}{ext}"
