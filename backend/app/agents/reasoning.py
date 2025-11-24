from typing import List
from ..langgraph.state import HRState, RetrievedChunk
from ..azure.openai_client import create_chat_completion


SYSTEM_PROMPT = """You are an internal HR assistant for a company.

Rules:
- Answer ONLY based on the provided HR policy context.
- If the answer is not in the context, say you don't know and recommend contacting HR.
- Cite your sources with (Document, page X) where possible.
- Be concise, clear, and professional.
"""


def _format_context(chunks: List[RetrievedChunk]) -> str:
    lines = []
    for i, c in enumerate(chunks):
        src = c.get("source", "unknown")
        page = c.get("page")
        lines.append(
            f"[{i}] Source: {src}, Page: {page}\n{c.get('content','')}\n"
        )
    return "\n\n".join(lines)


def generate_answer(state: HRState) -> HRState:
    question = state["question"]
    chunks = state.get("retrieved_chunks", [])

    context_text = _format_context(chunks)

    user_content = f"Question:\n{question}\n\nHR Policy Context:\n{context_text}"

    msg = [{"role": "user", "content": user_content}]
    answer = create_chat_completion(SYSTEM_PROMPT, msg, max_tokens=800)

    # Simple citation mapping: use all chunks as citations for now
    state["answer"] = answer
    state["citations"] = chunks
    state.setdefault("debug_info", {})
    state["debug_info"]["used_context_len"] = len(chunks)
    return state
