from ..langgraph.state import HRState
from ..azure.search_client import search_hr_documents


def build_filter_from_topic(topic: str | None) -> str | None:
    # Disable topic filtering since we don't have topic field in index
    # TODO: Add topic field to index schema if needed
    return None


def retrieve_documents(state: HRState) -> HRState:
    question = state["question"]
    topic = state.get("topic")

    # Use no filter for now since we don't have topic field
    docs = search_hr_documents(question, top_k=5, filters=None)

    chunks = []
    for d in docs:
        chunks.append({
            "content": d["content"],
            "source": d.get("source", "unknown"),
            "page": d.get("page"),
        })

    state["retrieved_chunks"] = chunks
    state.setdefault("debug_info", {})
    state["debug_info"]["retrieved_count"] = len(chunks)
    return state
