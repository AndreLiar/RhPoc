import streamlit as st


def init_chat():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []


def add_message(role: str, content: str):
    st.session_state["messages"].append({"role": role, "content": content})


def render_chat_history():
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])
