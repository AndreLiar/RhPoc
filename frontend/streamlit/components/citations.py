import streamlit as st


def render_citations(citations):
    if not citations:
        st.info("No citations available yet.")
        return

    for c in citations:
        with st.container():
            st.markdown(f"**📄 Source:** {c.get('source', 'Unknown')}")

            page = c.get("page")
            if page:
                st.markdown(f"**Page:** {page}")

            snippet = c.get("snippet")
            if snippet:
                st.markdown(
                    f"""
                    <div style="padding:8px; background:#F7F7F7; border-radius:6px; margin-bottom:10px;">
                        {snippet[:350]}...
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("---")
