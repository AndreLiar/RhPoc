import os

import requests
import streamlit as st
from dotenv import load_dotenv

from components.chat import add_message, init_chat, render_chat_history
from components.citations import render_citations
from components.header import render_header

# Load environment variables
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1/hr/query")
BACKEND_UPLOAD_URL = os.getenv(
    "BACKEND_UPLOAD_URL", "http://localhost:8000/api/v1/hr/upload"
)

st.set_page_config(
    page_title="HR Assistant AI",
    page_icon="💼",
    layout="wide"
)

render_header()

# Initialize Streamlit chat session
init_chat()

# -----------------------
# Sidebar: Upload docs + citations
# -----------------------
with st.sidebar:
    st.header("📁 Upload HR Documents")

    uploaded_files = st.file_uploader(
        "Upload HR policy PDFs",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        if st.button("Ingest documents"):
            results = []
            for f in uploaded_files:
                try:
                    file_bytes = f.read()
                    f.seek(0)
                    if not file_bytes:
                        continue
                    with st.spinner(f"Ingesting {f.name}..."):
                        files = {"file": (f.name, file_bytes, "application/pdf")}
                        resp = requests.post(
                            BACKEND_UPLOAD_URL, files=files, timeout=120
                        )
                        resp.raise_for_status()
                        results.append(resp.json())
                except Exception as e:
                    st.error(f"Error ingesting {f.name}: {e}")
            if results:
                st.success("Ingestion completed.")
                st.json(results)

    st.markdown("---")
    st.header("📚 Sources")
    citations = st.session_state.get("latest_citations", [])
    render_citations(citations)

# -----------------------
# Main Chat UI
# -----------------------
user_input = st.chat_input("Ask an HR question...")

if user_input:
    add_message("user", user_input)

    payload = {
        "question": user_input,
        "topic": None,
        "debug": False,
    }

    # Call backend
    try:
        with st.spinner("Thinking..."):
            response = requests.post(BACKEND_URL, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            answer = data.get("answer", "No answer received.")
            citations = data.get("citations", [])

            add_message("assistant", answer)

            # Store citations for sidebar display
            st.session_state["latest_citations"] = citations

    except Exception as e:
        st.error(f"Error contacting backend: {e}")

# Render chat
render_chat_history()
