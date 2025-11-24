from typing import List, TypedDict, Optional, Dict, Any


class RetrievedChunk(TypedDict, total=False):
    content: str
    source: str
    page: Optional[int]


class HRState(TypedDict, total=False):
    question: str
    topic: Optional[str]
    intent: Optional[str]
    retrieved_chunks: List[RetrievedChunk]
    answer: Optional[str]
    citations: List[RetrievedChunk]
    debug: bool
    debug_info: Dict[str, Any]
