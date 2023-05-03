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

        # cred = {"hawk-id": hawk_id, "password": password, "site-url": site_url}
        # if logged_in(cookie_manager, cred):
        #     time.sleep(0.2)
        #     cookie_manager.set("cred", cred)
        #     redirect("/Download%20File")
        #     return
        if result:
            #redirect("/Download%20File")
            st.experimental_rerun()
            return

        login_form.error("Invalid Login Credentials or Sharepoint Site URL")


def sign_out_form_render():
    st.title("Sign Out")
    st.write("Press sign out to log out of your sharepoint account")

#cookie_manager = get_manager()


if SHAREPOINT.is_signed_in():
    sign_out_form_render()
else:
    login_form_render()
