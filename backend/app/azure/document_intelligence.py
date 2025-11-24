from typing import List, Dict, Optional

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from loguru import logger

from ..config import get_settings

_settings = get_settings()

_client: Optional[DocumentAnalysisClient] = None


def _create_client() -> Optional[DocumentAnalysisClient]:
    if not _settings.AZURE_FORMRECOG_ENDPOINT or not _settings.AZURE_FORMRECOG_API_KEY:
        logger.debug("Azure Document Intelligence credentials not configured.")
        return None
    try:
        return DocumentAnalysisClient(
            endpoint=_settings.AZURE_FORMRECOG_ENDPOINT,
            credential=AzureKeyCredential(_settings.AZURE_FORMRECOG_API_KEY),
        )
    except Exception as exc:
        logger.error(f"Failed to initialize DocumentAnalysisClient: {exc}")
        return None


def get_document_analysis_client() -> Optional[DocumentAnalysisClient]:
    global _client
    if _client is None:
        _client = _create_client()
    return _client


def extract_pages_via_document_intelligence(pdf_bytes: bytes) -> List[Dict]:
    """Return [{"page": int, "text": str}] using Azure Document Intelligence."""

    client = get_document_analysis_client()
    if client is None:
        return []

    try:
        logger.info(f"Starting Document Intelligence analysis for {len(pdf_bytes)} bytes")
        poller = client.begin_analyze_document(
            model_id="prebuilt-read",
            document=pdf_bytes,
        )
        result = poller.result()
        logger.info(f"Document Intelligence analysis completed. Found {len(result.pages or [])} pages")
    except Exception as exc:
        logger.error(f"Document Intelligence extraction failed: {exc}")
        return []

    pages: List[Dict] = []
    for page in result.pages or []:
        lines = []
        for line in getattr(page, "lines", []) or []:
            content = (line.content or "").strip()
            if content:
                lines.append(content)
        page_text = " ".join(lines).strip()
        if page_text:
            pages.append({
                "page": page.page_number,
                "text": page_text,
            })

    return pages
