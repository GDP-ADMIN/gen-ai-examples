"""This module contains the file upload helper.

Authors:
    Muhammad Afif Al Hawari (muhammad.a.a.hawari@gdplabs.id)
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)
    Hubert Michael Sanyoto (hubert.m.sanyoto@gdplabs.id)
    Felicia Limanta (felicia.limanta@gdplabs.id)
    Dimitrij Ray (dimitrij.ray@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)

"""

import json
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any

import httpx
from fastapi import HTTPException, UploadFile

from claudia_gpt.api.helper.object_storage import (
    ObjectStorageHelper,
)
from claudia_gpt.chat_history.schemas import ConversationDocument
from claudia_gpt.config.constant import (
    DOCPROC_BACKEND_URL,
    OBJECT_STORAGE_TYPE,
    UploadedFileConstants,
)
from claudia_gpt.utils.file_utils import sanitize_file_name
from claudia_gpt.utils.logger import logger

DOCPROC_REQUEST_TIMEOUT = 600
FILE_INPUT_TYPE = "FILE"


@dataclass
class UploadedFile:
    """Represents data for a single uploaded file."""

    file_name: str  # original file name
    sanitized_file_name: str
    content: bytes
    content_type: str

    def as_httpx_files_tuple(self) -> tuple[str, tuple[str, bytes, str]]:
        """Convert the UploadedFile instance to the tuple format expected by httpx.

        Returns:
            tuple[str, tuple[str, bytes, str]]: The tuple format expected by httpx.
        """
        return "files", (self.sanitized_file_name, self.content, self.content_type)


async def forward_upload(
    conversation_id: str,
    knowledge_base_id: str,
    file_ids: list[str],
    uploaded_files: list[UploadedFile],
) -> bool:
    """Forward the uploaded files to the DocProc API.

    Args:
        conversation_id (str): The conversation ID.
        knowledge_base_id (str): The vector database index name.
        file_ids (list[str]): The conversation file ids.
        uploaded_files (list[UploadedFile]): The uploaded files data.

    Returns:
        bool: True if the files are successfully forwarded.
    """
    file_metadatas = [
        json.dumps(
            {
                "file_id": file_id,
                "input_type": FILE_INPUT_TYPE,
                "filename": uploaded_file.sanitized_file_name,
            }
        )
        for file_id, uploaded_file in zip(file_ids, uploaded_files, strict=True)
    ]
    data: dict[str, Any] = {
        "conversation_id": conversation_id,
        "file_metadatas": file_metadatas,
        "knowledge_base_id": knowledge_base_id,
    }

    httpx_files = [uploaded_file.as_httpx_files_tuple() for uploaded_file in uploaded_files]

    async with httpx.AsyncClient() as client:
        external_response = await client.post(
            f"{DOCPROC_BACKEND_URL}/add-documents",
            data=data,
            files=httpx_files,
            timeout=DOCPROC_REQUEST_TIMEOUT,
        )

    if external_response.status_code != HTTPStatus.OK:
        raise HTTPException(
            status_code=external_response.status_code,
            detail=f"Failed to forward the files to the DocProc API. Cause: {external_response.text}",
        )

    return True


async def parse_request_files(files: list[UploadFile]) -> list[UploadedFile]:
    """Parse request files into UploadedFile objects.

    Args:
        files (list[UploadFile]): List of files from the request.

    Returns:
        list[UploadedFile]: Parsed files ready for upload.
    """
    return [
        UploadedFile(
            file_name=str(file.filename),
            sanitized_file_name=sanitize_file_name(str(file.filename)),
            content=await file.read(),
            content_type=str(file.content_type),
        )
        for file in files
    ]


def create_metadata_attachments(
    uploaded_files: list[UploadedFile],
    conversation_documents: list[ConversationDocument],
) -> dict[str, list[dict[str, str | int]]]:
    """Process uploaded files and create metadata attachments.

    This function iterates through the uploaded files and conversation documents,
    and returns a dictionary of metadata attachments.

    Args:
        uploaded_files (list[UploadedFile]): Parsed uploaded files.
        conversation_documents (list[ConversationDocument]): List of conversation documents.

    Returns:
        dict[str, list[dict[str, str | int]]]: The metadata attachments in JSON format.
    """
    attachments: list[dict[str, str | int]] = []
    for uploaded_file, conversation_document in zip(uploaded_files, conversation_documents, strict=True):
        attachments.append(
            {
                "id": str(conversation_document.id),
                "name": uploaded_file.file_name,
                "type": uploaded_file.content_type,
                "size": len(uploaded_file.content),
                "objectStorageType": OBJECT_STORAGE_TYPE,
                "url": "",  # either the url was sent from the frontend or a presigned url from external storage
            }
        )
    return {"attachments": attachments}


async def store_file_and_get_object_key(
    uploaded_file: UploadedFile,
    conversation_document: ConversationDocument,
    conversation_id: str,
) -> str:
    """Store the files in the object storage and return the object key.

    Args:
        uploaded_file (UploadedFile): The uploaded file.
        conversation_document (ConversationDocument): The conversation document.
        conversation_id (str): The ID of the conversation associated with these files.

    Returns:
        str: The object key.
    """
    object_storage_helper = ObjectStorageHelper.get_instance()
    return await object_storage_helper.upload_from_uploaded_file(
        conversation_id=conversation_id,
        file_id=str(conversation_document.id),
        uploaded_file=uploaded_file,
    )


def validate_file_upload(uploaded_files: list[UploadedFile], max_file_size: int) -> None:
    """Validate the uploaded file size and count.

    Args:
        uploaded_files (list[UploadedFile]): The list of uploaded files.
        max_file_size (int): The maximum allowed file size.

    Raises:
        HTTPException: If the file size exceeds the maximum allowed size or
        if the number of uploaded files exceeds the limit.
    """
    if not uploaded_files:
        return

    if len(uploaded_files) > UploadedFileConstants.MAX_UPLOADED_FILE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=UploadedFileConstants.FILE_COUNT_EXCEEDED_MSG,
        )

    for uploaded_file in uploaded_files:
        if len(uploaded_file.content) > max_file_size:
            raise HTTPException(
                status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                detail=UploadedFileConstants.FILE_SIZE_EXCEEDED_MSG.format(max_file_size=max_file_size),
            )


def retrieve_file_content_from_storage(conversation_id: str, attachments: list[dict[str, Any]]) -> list[bytes]:
    """Retrieve file content from object storage.

    Args:
        conversation_id (str): The conversation ID.
        attachments (list[dict[str, Any]]): List of attachment metadata.

    Returns:
        list[bytes]: List of retrieved file content in bytes.
    """
    retrieved_files: list[bytes] = []
    object_storage_helper = ObjectStorageHelper.get_instance()
    for attachment in attachments:
        try:
            attachment_content: bytes | None = object_storage_helper.get_file_content_from_storage(
                conversation_id, attachment
            )
            if attachment_content:
                retrieved_files.append(attachment_content)
            else:
                logger.warning(f"Failed to read attachment: {attachment['name']}")
        except Exception as e:
            logger.error(f"Failed to retrieve attachment: {e}")
            raise Exception(f"Failed to retrieve attachment: {e}") from e

    return retrieved_files


def is_image_attachment_valid(attachment: dict[str, Any]) -> bool:
    """Check if the attachment is valid.

    Args:
        attachment (dict[str, Any]): The attachment metadata.

    Returns:
        bool: True if the attachment is valid, False otherwise.
    """
    required_fields = ["id", "name", "type", "size"]
    for field in required_fields:
        if not attachment.get(field):
            logger.warning(f"Attachment is missing required field: {field}")
            return False

    if not attachment["type"].startswith("image/"):
        return False

    if not isinstance(attachment["size"], int) or attachment["size"] <= 0:
        logger.warning(f"Image attachment has invalid size: {attachment['size']}")
        return False

    return True
