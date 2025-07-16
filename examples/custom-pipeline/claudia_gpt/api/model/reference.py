"""Reference models.

Authors:
    Ryan Ignatius Hadiwijaya (ryan.i.hadiwijaya@gdplabs.id)

References:
    None
"""

from typing import Any

from pydantic import BaseModel


class ReferenceMetadata(BaseModel):
    """A class to represent metadata for a reference.

    Attributes:
        source_type (str): The type of the source.
        source (str): The source of the reference.
        file_id (str): The id of the file associated with the reference.
        conversation_id (str): The id of the conversation associated with the reference.
        content (str): The content of the reference.
        title (str): The title of the reference.
        source_url (str | None): The optional source url of the reference.
        link (str | None): The optional link of the reference.
        gdrive_link (str | None): The optional gdrive_link of the reference.
        transcripts (list[dict[str, Any]] | None): A list of transcript objects,
            each containing various fields, including `start_time` as a float.
        position (list[dict[str, Any]] | None): A list of position objects,
            each containing various fields, including `coordinates` as a float array.
    """

    source_type: str = ""
    source: str = ""
    file_id: str = ""
    conversation_id: str = ""
    content: str = ""
    title: str = ""
    source_url: str | None = None
    link: str | None = None
    gdrive_link: str | None = None
    transcripts: list[dict[str, Any]] | None = None
    position: list[dict[str, Any]] | None = None
    heading_1: str | None = None
    heading_2: str | None = None


class ReferenceResponse(BaseModel):
    """Response model for reference.

    Attributes:
        id (str): The id of the reference.
        title (str): The title of the reference.
        name (str): The name of the reference.
        type (str): The type of the reference (e.g., audio, pdf, website).
        content (str): The content of the reference.
        url (str): The URL of the reference.
        embed_url (str | None): The embed URL of the reference.
        transcripts (list[dict[str, Any]] | None): A list of transcript objects,
            each containing various fields, including `start_time` as a float.
        position (list[dict[str, Any]] | None): A list of position objects,
            each containing various fields, including `coordinates` as a float array.
    """

    id: str
    title: str
    name: str
    type: str
    content: str
    url: str
    embed_url: str | None = None
    transcripts: list[dict[str, Any]] | None = None
    position: list[dict[str, Any]] | None = None
