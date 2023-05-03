"""
Signs the user into SharePoint
"""
import streamlit as st

from src.managers.sharepoint.sharepoint_session import SharepointSession

SHAREPOINT = SharepointSession(st.session_state)

def login_form_render():
    """
    Sets up the login and connection form
    :return:
    """

    st.title("Log In")

    login_form = st.form('sharepoint-login-form')

    hawk_id = login_form.text_input("HawkID", key="hawkid-username", placeholder="HawkID@uiowa.edu")

    password = login_form.text_input("HawkID Password", key="hawkid-password", placeholder="HawkID Password",
                                     type="password")

    login_button = login_form.form_submit_button("Log in to Sharepoint Site")

    if login_button:
        result = SHAREPOINT.login(hawk_id, password)

        if result:
            SHAREPOINT.set_redirect("/")
            st.experimental_rerun()

        login_form.error("Invalid Login Credentials or Sharepoint Site URL")

def sign_out_form_render():
    '''
    Renders the sign out form shown when user is logged in.
    '''
    st.title("Sign Out")
    st.write("Press sign out to log out of your sharepoint account")

if SHAREPOINT.is_signed_in():
    sign_out_form_render()
else:
    login_form_render()
