"""
Handler for cookies for SharePoint Login
"""
import extra_streamlit_components as stx


def get_manager():
    """
    Cookie Manager
    :return: Cookie Manager, to access login creds
    """
    return stx.CookieManager()
