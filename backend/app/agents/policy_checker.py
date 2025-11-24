from ..langgraph.state import HRState

# For now, this node is a placeholder.
# Enterprise can plug compliance checks, PII filters, etc.


def policy_check(state: HRState) -> HRState:
    # Example: we could scan for forbidden patterns, but we'll just pass-through.
    # You can add flags in state["debug_info"]["policy_check"] later.
    state.setdefault("debug_info", {})
    state["debug_info"]["policy_check"] = "passed"
    return state
