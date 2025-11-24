from langgraph.graph import StateGraph, END
from .state import HRState
from ..agents.input_classifier import classify_intent
from ..agents.retriever import retrieve_documents
from ..agents.reasoning import generate_answer
from ..agents.policy_checker import policy_check


def build_hr_assistant_graph():
    graph = StateGraph(HRState)

    # Nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_docs", retrieve_documents)
    graph.add_node("generate_answer", generate_answer)
    graph.add_node("policy_check", policy_check)

    # Edges
    graph.set_entry_point("classify_intent")
    graph.add_edge("classify_intent", "retrieve_docs")
    graph.add_edge("retrieve_docs", "generate_answer")
    graph.add_edge("generate_answer", "policy_check")
    graph.add_edge("policy_check", END)

    return graph.compile()


# Singleton compiled app
hr_assistant_app = build_hr_assistant_graph()
