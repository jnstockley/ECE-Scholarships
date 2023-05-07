"""
Compilation of functions for simplifying common html generation
"""

import streamlit as st


def centered_text(msg):
    """Generates HTML to center text"""
    return f'<div style="text-align: center;">{msg}</div>'


def redirect(url: str):
    """
    Helper function to redirect if not signed in
    :param url: URL to redirect to
    """
    st.write(
        f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True
    )
