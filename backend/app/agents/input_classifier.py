from typing import Dict
from ..azure.openai_client import create_chat_completion
from ..langgraph.state import HRState


SYSTEM_PROMPT = """You are an HR query classifier.

Given a user question, you MUST:
- detect the high-level topic (one of: leave, benefits, payroll, conduct, remote_work, harassment, equipment, onboarding, generic)
- detect the intent (one of: ask_policy, ask_procedure, ask_definition, summarize, generic)

Return a JSON object with keys: topic, intent.
Return ONLY valid JSON, nothing else.
"""


def classify_intent(state: HRState) -> HRState:
    question = state["question"]
    msg = [{"role": "user", "content": question}]

    import json
    raw = create_chat_completion(SYSTEM_PROMPT, msg, max_tokens=200)

    topic = "generic"
    intent = "generic"

    try:
        data: Dict = json.loads(raw)
        topic = data.get("topic", topic)
        intent = data.get("intent", intent)
    except Exception:
        pass

    state["topic"] = topic
    state["intent"] = intent
    state.setdefault("debug_info", {})
    state["debug_info"]["classifier_raw"] = raw

    return state
