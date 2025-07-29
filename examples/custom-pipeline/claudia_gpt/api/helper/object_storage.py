"""A helper class to interact with ObjectStorage.

This class provides methods to interact with ObjectStorage, such as uploading files.

Authors:
    Ryan Ignatius Hadiwijaya (ryan.i.hadiwijaya@gdplabs.id)
    Felicia Limanta (felicia.limanta@gdplabs.id)
"""

import datetime
import io
from typing import TYPE_CHECKING

import httpx
from minio import Minio
from minio.commonconfig import CopySource
from minio.error import S3Error
from pydantic import BaseModel

from claudia_gpt.chat_history import ChatHistoryStorage
from claudia_gpt.chat_history.schemas import (
    Message,
    ObjectStorageType,
)
from claudia_gpt.config.constant import (
    OBJECT_STORAGE_BUCKET,
    OBJECT_STORAGE_PASSWORD,
    OBJECT_STORAGE_SECURE,
    OBJECT_STORAGE_TYPE,
    OBJECT_STORAGE_URL,
    OBJECT_STORAGE_USER,
    ConversationConstants,
)
from claudia_gpt.utils.file_utils import sanitize_file_name
from claudia_gpt.utils.initializer import (
    get_chat_history_storage,
)
from claudia_gpt.utils.logger import logger

if TYPE_CHECKING:
    from claudia_gpt.api.helper.message.file_upload import UploadedFile


class ObjectStorageDeleteRequest(BaseModel):
    """Request model for deleting a file in object storage."""

    user_id: str
    conversation_id: str
    file_id: str
    file_name: str
    object_storage_type: str
    chatbot_ids: list[str]


class ObjectStorageHelper:
    """A helper class to interact with ObjectStorage."""

    _instance = None
    bucket: str
    client: Minio
    chat_history_storage: ChatHistoryStorage

    def __init__(self, bucket: str, client: Minio, chat_history_storage: ChatHistoryStorage):
        """Initialize an instance of ObjectStorageHelper.

        This method initializes an instance of ObjectStorageHelper with the provided bucket name and client.
        It sets the bucket and client attributes of the instance.

        Args:
            bucket (str): The name of the bucket in the object storage.
            client (Minio): An instance of Minio client to interact with the object storage.
            chat_history_storage (ChatHistoryStorage): An instance of ChatHistoryStorage.

        Returns:
            None
        """
        self.bucket = bucket
        self.client = client
        self.chat_history_storage = chat_history_storage

    @classmethod
    def get_instance(cls) -> "ObjectStorageHelper":
        """Get an instance of the ObjectStorageHelper class.

        Returns:
            ObjectStorageHelper: An instance of the ObjectStorageHelper class.
        """
        if cls._instance is None:
            try:
                if OBJECT_STORAGE_TYPE == ObjectStorageType.MINIO.value:
                    cls._instance = ObjectStorageHelper(
                        OBJECT_STORAGE_BUCKET,
                        Minio(
                            OBJECT_STORAGE_URL,
                            access_key=OBJECT_STORAGE_USER,
                            secret_key=OBJECT_STORAGE_PASSWORD,
                            secure=OBJECT_STORAGE_SECURE,
                        ),
                        get_chat_history_storage(),
                    )
                else:
                    logger.warning(f"Unsupported OBJECT_STORAGE_TYPE: {OBJECT_STORAGE_TYPE}")
                    raise ValueError(f"Unsupported OBJECT_STORAGE_TYPE: {OBJECT_STORAGE_TYPE}")
            except S3Error as e:
                logger.warning(f"Failed to initialize {OBJECT_STORAGE_TYPE} client: {e}")
                raise RuntimeError(f"Failed to initialize {OBJECT_STORAGE_TYPE} client due to S3 error: {e}") from e
            except Exception as e:
                logger.warning(f"Unexpected error during {OBJECT_STORAGE_TYPE} client initialization: {e}")
                raise RuntimeError(f"Unexpected error during {OBJECT_STORAGE_TYPE} client initialization: {e}") from e

        return cls._instance

    async def upload_from_uploaded_file(
        self,
        conversation_id: str,
        file_id: str,
        uploaded_file: "UploadedFile",
    ) -> str:
        """Upload a file from an UploadedFile instance to the object storage bucket.

        Args:
            conversation_id (str): The ID of the conversation associated with the file.
            file_id (str): The unique identifier for the file.
            uploaded_file (UploadedFile): The uploaded file.

        Returns:
            str: The object key.
        """
        return await self.upload(
            conversation_id=conversation_id,
            file_id=file_id,
            file_name=uploaded_file.file_name,
            file_stream=uploaded_file.content,
            file_type=uploaded_file.content_type,
        )

    def _generate_object_key(
        self,
        conversation_id: str,
        file_id: str,
    ) -> str:
        """Generate a unique object key for storing files in the object storage.

        Args:
            conversation_id (str): The ID of the conversation.
            file_id (str): The unique identifier for the file.

        Returns:
            str: A formatted object key.
        """
        return f"{conversation_id}/{file_id}"

    def get_conversation_document_object_key(
        self,
        conversation_id: str,
        file_id: str,
    ) -> str | None:
        """Get the object key for a conversation document.

        Args:
            conversation_id (str): The ID of the conversation.
            file_id (str): The ID of the conversation document.

        Returns:
            str | None: The object key for the conversation document or None if not exists.
        """
        conversation_document = self.chat_history_storage.get_conversation_document(file_id)
        if not conversation_document:
            return None

        if not conversation_document.object_key:
            # For legacy attachments, generate the object key using the old format
            object_key = f"{conversation_id}/{file_id}"
            conversation_document = self.chat_history_storage.update_conversation_document(
                document_id=conversation_document.id,
                status=conversation_document.status.value,
                number_of_chunks=conversation_document.number_of_chunks,
                message=conversation_document.message,
                object_key=object_key,
            )

        return conversation_document.object_key

    async def upload(
        self,
        conversation_id: str,
        file_id: str,
        file_name: str,
        file_stream: bytes,
        file_type: str,
    ) -> str:
        """Upload a file to the specified object storage bucket.

        Args:
            conversation_id (str): The ID of the conversation associated with the file.
            file_id (str): The unique identifier for the file.
            file_name (str): The name of the file to be uploaded.
            file_stream (bytes): The byte stream of the file content to be uploaded.
            file_type (str): The type of the file.

        Returns:
            str: This method returns object key. It raises exceptions if the upload fails.
        """
        sanitized_file_name = sanitize_file_name(file_name)
        logger.info(f"Uploading file '{file_name}' (Sanitized: {sanitized_file_name}) to bucket '{self.bucket}'")

        if not self.client:
            logger.warning(f"Object storage client {OBJECT_STORAGE_TYPE} is not initialized.")
            raise ValueError(f"Object storage client {OBJECT_STORAGE_TYPE} is not provided.")

        if not self.client.bucket_exists(self.bucket):
            logger.info(
                f"Bucket '{self.bucket}' does not exist in object storage {OBJECT_STORAGE_TYPE}. "
                f"Attempting to create it."
            )
            self.client.make_bucket(self.bucket)

        object_key = self._generate_object_key(conversation_id, file_id)

        try:
            file_stream = io.BytesIO(file_stream)
            file_length = len(file_stream.getbuffer())

            if file_length == 0:
                logger.warning(f"File '{file_name}' (Sanitized: {sanitized_file_name}) is empty. Aborting upload.")
                raise ValueError(f"File '{file_name}' (Sanitized: {sanitized_file_name}) is empty. Aborting upload.")

            if OBJECT_STORAGE_TYPE == ObjectStorageType.MINIO.value:
                self.client.put_object(
                    bucket_name=self.bucket,
                    object_name=object_key,
                    data=file_stream,
                    length=file_length,
                    content_type=file_type,
                    metadata={
                        "conversation_id": conversation_id,
                        "file_id": file_id,
                        "file_name": sanitized_file_name,
                    },
                )
            else:
                logger.warning(f"Unsupported object storage type: {OBJECT_STORAGE_TYPE}")
                raise ValueError(f"Unsupported object storage type: {OBJECT_STORAGE_TYPE}")

            logger.info(
                f"'{file_name}' (Sanitized: {sanitized_file_name}) is successfully uploaded to bucket "
                f"'{self.bucket}' as '{object_key}'"
            )
            return object_key
        except ValueError as e:
            logger.warning(f"File value error during file upload: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP error occurred during file upload: {e}")
            raise
        except S3Error as e:
            logger.warning(f"S3 error occurred during file upload: {e}")
            raise
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"Network error during file upload: {e}")
            raise RuntimeError("Network error occurred during file upload") from e
        except OSError as e:
            logger.warning(f"File system error during file upload: {e}")
            raise RuntimeError("File system error occurred during file upload") from e
        except Exception as e:
            logger.warning(f"Unexpected error during file upload: {e}")
            raise RuntimeError("An unexpected error occurred during file upload") from e

    def generate_presigned_url(
        self,
        conversation_id: str,
        file_id: str,
        file_name: str,
        file_type: str,
        expires: int = 24,
    ) -> str:
        """Generate a presigned URL to access a file in the object storage.

        Args:
            conversation_id (str): The ID of the conversation associated with the file.
                                   This will be the folder name of the file inside the object storage.
            file_id (str): The unique identifier for the document.
            file_name (str): The name of the file for inline response.
            file_type (str): The type of the file.
            expires (int): The number of hours the presigned URL is valid for. Default is 24 hours (1 day).

        Returns:
            str: A presigned URL to access the file.
        """
        if expires <= 0:
            raise ValueError("Expiration time must be positive")

        logger.info(
            f"Generating presigned URL for file '{file_name}' "
            f"(Sanitized: {sanitize_file_name(file_name)}) "
            f"with ID: {file_id} in conversation '{conversation_id}' "
            f"within bucket '{self.bucket}'. "
            f"URL will be valid for {expires} hours."
        )
        object_key = self.get_conversation_document_object_key(conversation_id, file_id)

        try:
            if OBJECT_STORAGE_TYPE == ObjectStorageType.MINIO.value:
                presigned_url = self.client.presigned_get_object(
                    bucket_name=self.bucket,
                    object_name=object_key,
                    expires=datetime.timedelta(hours=expires),
                    response_headers={
                        "response-content-type": file_type,
                        "response-content-disposition": f'inline; filename="{file_name}"',
                    },
                )
            else:
                logger.warning(f"Unsupported object storage type: {OBJECT_STORAGE_TYPE}")
                raise ValueError(f"Unsupported object storage type: {OBJECT_STORAGE_TYPE}")

            logger.info(f"Presigned URL generated: {presigned_url}")
            return presigned_url
        except S3Error as e:
            logger.warning(f"Error occurred while generating presigned URL: {e}")
            raise RuntimeError(f"Failed to generate presigned URL: {e}") from e
        except Exception as e:
            logger.warning(f"Unexpected error while generating presigned URL: {e}")
            raise RuntimeError(f"An unexpected error occurred while generating presigned URL: {e}") from e

    def generate_presigned_urls_for_attachments(
        self,
        attachments: list[dict[str, str | int]],
        conversation_id: str,
    ) -> list[dict[str, str | int]]:
        """Generate presigned URLs for attachments.

        Args:
            attachments (list[dict[str, str | int]]): The metadata attachments in JSON format.
            conversation_id (str): The conversation ID.

        Returns:
            list[dict[str, str | int]]: Attachments with presigned URLs added.
        """
        attachments = [
            {
                **attachment,
                "url": self.generate_presigned_url(
                    conversation_id=conversation_id,
                    file_id=str(attachment["id"]),
                    file_name=str(attachment["name"]),
                    file_type=str(attachment["type"]),
                ),
            }
            for attachment in attachments
            if attachment.get("objectStorageType")
        ]
        return attachments

    def generate_presigned_urls_for_attachments_in_messages(
        self, chat_messages: list[Message], conversation_id: str
    ) -> list[dict[str, str | int]]:
        """Generate presigned URLs for attachments in chat messages and update the message metadata.

        Args:
            chat_messages (list[Message]): The chat messages.
            conversation_id (str): The conversation ID.

        Returns:
            list[dict[str, str | int]]: A list of dictionaries containing the file details.
        """
        attachments: list[dict[str, str | int]] = []
        for message in chat_messages:
            if not hasattr(message, "metadata_") or not message.metadata_:
                continue

            message_attachments = message.metadata_.get("attachments", [])
            if message_attachments:
                updated_attachments = self.generate_presigned_urls_for_attachments(
                    attachments=message_attachments,
                    conversation_id=conversation_id,
                )
                message.metadata_["attachments"] = updated_attachments
                attachments.extend([attachment for attachment in updated_attachments if attachment not in attachments])
        return attachments

    def delete(  # pylint: disable=too-many-positional-arguments
        self, object_storage_delete_request: ObjectStorageDeleteRequest
    ) -> None:
        """Delete a file from the specified object storage bucket.

        Args:
            object_storage_delete_request (ObjectStorageDeleteRequest): An object containing the request details

        Returns:
            None: This method does not return a value. It raises exceptions if the deletion fails.
        """
        valid_conversation = self.chat_history_storage.get_conversation(
            object_storage_delete_request.user_id, object_storage_delete_request.conversation_id
        )
        if not valid_conversation:
            logger.warning(
                f"User {object_storage_delete_request.user_id} does not have access "
                f"to conversation {object_storage_delete_request.conversation_id}."
            )
            raise ValueError(ConversationConstants.ERR_NOT_FOUND_MSG)

        if valid_conversation.chatbot_id not in object_storage_delete_request.chatbot_ids:
            logger.warning(
                f"User {object_storage_delete_request.user_id} does not have access "
                f"to chatbot {valid_conversation.chatbot_id}."
            )
            raise ValueError("Chatbot not found")

        logger.info(f"Deleting file '{object_storage_delete_request.file_name}' from bucket '{self.bucket}'")

        if not self.client:
            logger.warning(f"{OBJECT_STORAGE_TYPE} client is not initialized.")
            raise ValueError(f"{OBJECT_STORAGE_TYPE} client is not provided.")

        object_key = self.get_conversation_document_object_key(
            object_storage_delete_request.conversation_id,
            object_storage_delete_request.file_id,
        )

        try:
            if OBJECT_STORAGE_TYPE == object_storage_delete_request.object_storage_type:
                if object_storage_delete_request.object_storage_type == ObjectStorageType.MINIO.value:
                    self.client.remove_object(
                        bucket_name=self.bucket,
                        object_name=object_key,
                    )
                else:
                    logger.warning(
                        f"Unsupported object storage type of file: {object_storage_delete_request.object_storage_type}"
                    )
                    raise ValueError(
                        f"Unsupported object storage type of file: {object_storage_delete_request.object_storage_type}"
                    )
            else:
                logger.warning(
                    f"Object storage type of file: {object_storage_delete_request.object_storage_type} "
                    f"is not compatible with object storage type available: {OBJECT_STORAGE_TYPE}"
                )
                raise ValueError("Object storage type of file is not compatible with object storage type available")

            logger.info(
                f"'{object_storage_delete_request.file_name}' is successfully deleted from bucket '{self.bucket}'"
            )
        except S3Error as e:
            logger.warning(f"S3 error occurred during file deletion: {e}")
            raise
        except Exception as e:
            logger.warning(f"Unexpected error during file deletion: {e}")
            raise RuntimeError("An unexpected error occurred during file deletion") from e

    def delete_by_object_key(self, object_key: str) -> None:
        """Delete a file from the specified object storage bucket.

        Args:
            object_key (str): The object key of the file to delete

        Returns:
            None: This method does not return a value. It raises exceptions if the deletion fails.
        """
        logger.info(f"Deleting file '{object_key}' from bucket '{self.bucket}'")

        if not self.client:
            logger.warning(f"{OBJECT_STORAGE_TYPE} client is not initialized.")
            raise ValueError(f"{OBJECT_STORAGE_TYPE} client is not provided.")

        try:
            self.client.remove_object(
                bucket_name=self.bucket,
                object_name=object_key,
            )
            logger.info(f"'{object_key}' is successfully deleted from bucket '{self.bucket}'")
        except S3Error as e:
            logger.warning(f"S3 error occurred during file deletion: {e}")
            raise
        except Exception as e:
            logger.warning(f"Unexpected error during file deletion: {e}")
            raise RuntimeError("An unexpected error occurred during file deletion") from e

    def delete_all_attachments_from_messages(
        self, user_id: str, messages: list[Message], chatbot_ids: list[str]
    ) -> None:
        """Delete all attachments from object storage for a list of messages.

        Args:
            user_id (str): The ID of the user attempting to delete the file.
            messages (list[Message]): A list of Message objects containing metadata with attachments.
            chatbot_ids (list[str]): The list of chatbot IDs that the user has access to.
        """
        for message in messages:
            if message.metadata_ and message.metadata_.get("attachments"):
                for attachment in message.metadata_["attachments"]:
                    try:
                        object_storage_delete_request = ObjectStorageDeleteRequest(
                            user_id=user_id,
                            conversation_id=message.conversation_id,
                            file_id=attachment["id"],
                            file_name=attachment["name"],
                            object_storage_type=attachment["objectStorageType"],
                            chatbot_ids=chatbot_ids,
                        )
                        self.delete(object_storage_delete_request)
                        logger.info(f"Deleted {attachment['name']} from object storage.")
                    except Exception as e:
                        logger.error(f"Failed to delete {attachment['name']}: {e}")

    def get_file_content_from_storage(self, conversation_id: str, attachment: dict[str, str | int]) -> bytes | None:
        """Get the file content from the object storage.

        Args:
            conversation_id (str): The conversation ID.
            attachment (dict[str, str | int]): The attachment metadata.

        Returns:
            bytes: The file content.
        """
        object_key = self.get_conversation_document_object_key(conversation_id, str(attachment.get("id", "")))
        if not object_key:
            logger.error(f"Object key not found for attachment {attachment['id']}")
            return None
        try:
            with self.client.get_object(bucket_name=self.bucket, object_name=object_key) as file_stream:
                file_content = file_stream.read()
                if not file_content:
                    logger.error(f"File content is empty for attachment {attachment['id']}. Skipping...")
                    return None
                logger.info(f"Retrieved file for attachment {attachment['id']} with size {len(file_content)} bytes")
        except Exception as e:
            logger.error(f"Failed to retrieve file for attachment {attachment['id']}: {e}")
            return None

        return file_content

    def get_file_content_by_object_key(self, object_key: str) -> tuple[bytes, str] | None:
        """Get the file content from the object storage.

        Args:
            object_key (str): The object key.

        Returns:
            bytes: The file content.
            str: The content type.
        """
        try:
            with self.client.get_object(bucket_name=self.bucket, object_name=object_key) as file_stream:
                file_content = file_stream.read()
                if not file_content:
                    logger.error(f"File content is empty for object key: {object_key}")
                    return None
                logger.info(f"Retrieved file for object key: {object_key} with size {len(file_content)} bytes")

                content_type = file_stream.headers.get("Content-Type")
                if not content_type:
                    logger.error(f"Content type is not found for object key: {object_key}")
                    return None

                return file_content, content_type
        except Exception as e:
            logger.error(f"Failed to retrieve file for object key: {object_key}: {e}")
            return None

    def _validate_source_object_exists(self, source_key: str) -> None:
        """Validate that the source object exists in the bucket.

        Args:
            source_key (str): The source object key to validate.

        Raises:
            ValueError: If the source object does not exist.
            RuntimeError: If there's an error validating the source object.
        """
        try:
            self.client.stat_object(bucket_name=self.bucket, object_name=source_key)
        except S3Error as e:
            if e.code == "NoSuchKey":
                logger.warning(f"Source object '{source_key}' does not exist")
                raise ValueError(f"Source object '{source_key}' does not exist") from e
            else:
                logger.warning(f"Error checking source object '{source_key}': {e}")
                raise RuntimeError(f"Failed to verify source object '{source_key}'") from e

    def copy_object(self, source_key: str, target_key: str) -> None:
        """Copy an object from one location to another within the same bucket.

        Args:
            source_key (str): The source object key.
            target_key (str): The target object key.

        Returns:
            None: This method does not return a value. It raises exceptions if the copy fails.
        """
        logger.info(f"Copying object from '{source_key}' to '{target_key}' in bucket '{self.bucket}'")

        if not self.client:
            logger.warning(f"Object storage client {OBJECT_STORAGE_TYPE} is not initialized.")
            raise ValueError(f"Object storage client {OBJECT_STORAGE_TYPE} is not provided.")

        if OBJECT_STORAGE_TYPE != ObjectStorageType.MINIO.value:
            logger.warning(f"Unsupported object storage type: {OBJECT_STORAGE_TYPE}")
            raise ValueError(f"Unsupported object storage type: {OBJECT_STORAGE_TYPE}")

        self._validate_source_object_exists(source_key)

        try:
            self.client.copy_object(
                bucket_name=self.bucket,
                object_name=target_key,
                source=CopySource(self.bucket, source_key),
            )
            logger.info(f"Object successfully copied from '{source_key}' to '{target_key}' in bucket '{self.bucket}'")
        except S3Error as e:
            logger.warning(f"S3 error occurred during object copy: {e}")
            raise
        except Exception as e:
            logger.warning(f"Unexpected error during object copy: {e}")
            raise RuntimeError("An unexpected error occurred during object copy") from e
