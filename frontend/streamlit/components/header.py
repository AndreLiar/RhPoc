import streamlit as st


def render_header():
    st.markdown("""
        <h1 style="text-align:center; margin-bottom:10px;">
            💼 HR Assistant AI
        </h1>
        <p style="text-align:center; opacity:0.8;">
            Ask HR questions • Get grounded answers • Verified by HR policies
        </p>
        <hr>
    """, unsafe_allow_html=True)
