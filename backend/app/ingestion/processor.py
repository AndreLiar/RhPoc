import uuid
from io import BytesIO
from typing import Dict, List, Tuple

import pypdf
import tiktoken
from loguru import logger

from ..azure.openai_client import create_embeddings
from ..azure.search_client import get_search_client
from ..azure.document_intelligence import extract_pages_via_document_intelligence


_encoder = tiktoken.encoding_for_model("gpt-4o")


def _chunk_text(text: str, max_tokens: int = 700) -> List[str]:
    tokens = _encoder.encode(text)
    chunks: List[str] = []

    for i in range(0, len(tokens), max_tokens):
        sub_tokens = tokens[i: i + max_tokens]
        chunks.append(_encoder.decode(sub_tokens))

    return chunks


def _extract_pages_from_pdf(pdf_bytes: bytes) -> List[Dict]:
    """
    Returns list of {"page": int, "text": str}
    """

    reader = pypdf.PdfReader(BytesIO(pdf_bytes))
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        clean_text = text.replace("\n", " ").strip()
        if clean_text:
            pages.append({"page": i + 1, "text": clean_text})

    return pages


def _extract_pages(pdf_bytes: bytes) -> Tuple[List[Dict], str]:
    # Force pypdf extraction for now to bypass Document Intelligence limitations
    logger.info("Using pypdf extraction to get all pages")
    pypdf_pages = _extract_pages_from_pdf(pdf_bytes)
    logger.info(f"pypdf returned {len(pypdf_pages)} pages")
    if pypdf_pages:
        return pypdf_pages, "pypdf"
    
    # Fallback to Document Intelligence if pypdf fails
    try:
        logger.info(f"Falling back to Document Intelligence extraction for {len(pdf_bytes)} bytes")
        di_pages = extract_pages_via_document_intelligence(pdf_bytes)
        logger.info(f"Document Intelligence returned {len(di_pages)} pages")
        return di_pages, "document_intelligence"
    except Exception as exc:
        logger.error(f"Document Intelligence extraction error: {exc}")
        return [], "failed"


def ingest_pdf_bytes(pdf_bytes: bytes, filename: str) -> Dict:
    """
    Full ingestion:
    - extract text per page
    - chunk
    - embed
    - upload to Azure Search
    """

    pages, extraction_method = _extract_pages(pdf_bytes)

    if not pages:
        return {
            "status": "no_text",
            "file": filename,
            "pages": 0,
            "chunks": 0,
            "failed": 0,
            "extraction_method": extraction_method,
        }

    docs_for_index = []
    all_texts = []

    for page_info in pages:
        page_number = page_info["page"]
        text = page_info["text"]

        chunks = _chunk_text(text, max_tokens=700)

        for chunk in chunks:
            doc_id = str(uuid.uuid4())
            docs_for_index.append(
                {
                    "id": doc_id,
                    "content": chunk,
                    "source": filename,
                    "page": page_number,
                }
            )
            all_texts.append(chunk)

    if not docs_for_index:
        return {
            "status": "no_chunks",
            "file": filename,
            "pages": len(pages),
            "chunks": 0,
            "failed": 0,
            "extraction_method": extraction_method,
        }

    embeddings = create_embeddings(all_texts)

    for doc, emb in zip(docs_for_index, embeddings):
        doc["embedding"] = emb

    search_client = get_search_client()
    results = search_client.upload_documents(docs_for_index)

    failed = len([r for r in results if not r.succeeded])

    return {
        "status": "ok" if failed == 0 else "partial",
        "file": filename,
        "pages": len(pages),
        "chunks": len(docs_for_index),
        "failed": failed,
        "extraction_method": extraction_method,
    }
