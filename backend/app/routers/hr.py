from fastapi import APIRouter, File, HTTPException, UploadFile

from ..azure.blob_client import upload_pdf_to_blob
from ..ingestion.processor import ingest_pdf_bytes
from ..langgraph.hr_graph import hr_assistant_app
from ..langgraph.state import HRState
from ..models.schemas import Citation, HRQueryRequest, HRQueryResponse

router = APIRouter()


@router.post("/query", response_model=HRQueryResponse)
async def query_hr_assistant(payload: HRQueryRequest):
    initial_state: HRState = {
        "question": payload.question,
        "topic": payload.topic,
        "debug": payload.debug,
        "retrieved_chunks": [],
        "citations": [],
        "debug_info": {},
    }

    final_state = hr_assistant_app.invoke(initial_state)

    answer = final_state.get("answer", "")
    citations_raw = final_state.get("citations", [])
    topic = final_state.get("topic")
    intent = final_state.get("intent")
    debug_info = final_state.get("debug_info", {})

    citations = [
        Citation(
            source=c.get("source", "unknown"),
            page=c.get("page"),
            snippet=c.get("content")[:300] if c.get("content") else None,
        )
        for c in citations_raw
    ]

    return HRQueryResponse(
        answer=answer,
        citations=citations,
        topic=topic,
        intent=intent,
        raw_context_count=len(citations_raw),
        debug_info=debug_info if payload.debug else None,
    )


@router.post("/upload")
async def upload_hr_document(file: UploadFile = File(...)):
    """Upload a single HR PDF, ingest into Azure Search. GitOps test."""

    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    blob_url = upload_pdf_to_blob(file.filename, pdf_bytes)
    stats = ingest_pdf_bytes(pdf_bytes, file.filename)

    return {
        "message": "Ingestion completed",
        "file": stats.get("file"),
        "status": stats.get("status"),
        "pages": stats.get("pages"),
        "chunks": stats.get("chunks"),
        "failed": stats.get("failed"),
        "extraction_method": stats.get("extraction_method"),
        "blob_url": blob_url,
    }
