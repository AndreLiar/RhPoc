import uuid
from typing import Optional

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, ContentSettings
from loguru import logger

from ..config import get_settings

_settings = get_settings()

_blob_service_client: Optional[BlobServiceClient] = None
_container_client = None


def _initialize_blob_service_client() -> Optional[BlobServiceClient]:
    if not _settings.AZURE_BLOB_CONNECTION_STRING:
        logger.debug("Azure Blob connection string not configured.")
        return None
    try:
        return BlobServiceClient.from_connection_string(
            _settings.AZURE_BLOB_CONNECTION_STRING
        )
    except Exception as exc:
        logger.error(f"Failed to initialize BlobServiceClient: {exc}")
        return None


def _ensure_container_client():
    global _blob_service_client, _container_client

    if _container_client is not None:
        return _container_client

    if not _settings.AZURE_STORAGE_CONTAINER:
        logger.debug("Azure Blob container name not configured.")
        return None

    if _blob_service_client is None:
        _blob_service_client = _initialize_blob_service_client()

    if _blob_service_client is None:
        return None

    try:
        container_client = _blob_service_client.get_container_client(
            _settings.AZURE_STORAGE_CONTAINER
        )
        try:
            container_client.create_container()
        except ResourceExistsError:
            pass
        _container_client = container_client
    except Exception as exc:
        logger.error(f"Failed to get/create container client: {exc}")
        _container_client = None

    return _container_client


def upload_pdf_to_blob(filename: str, data: bytes) -> Optional[str]:
    """Upload PDF bytes to blob storage if configured. Returns blob URL or None."""

    container_client = _ensure_container_client()
    if container_client is None:
        return None

    blob_name = f"{uuid.uuid4()}-{filename}"
    blob_client = container_client.get_blob_client(blob=blob_name)

    try:
        blob_client.upload_blob(
            data,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/pdf"),
        )
        return blob_client.url
    except Exception as exc:
        logger.error(f"Failed to upload blob {blob_name}: {exc}")
        return None
