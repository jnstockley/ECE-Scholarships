"""
Signs the user into SharePoint
"""
import time

import streamlit as st

from src.utils.sharepoint import get_manager, logged_in
from src.utils.html import redirect


def login_form_func():
    """
    Sets up the login and connection form
    :return:
    """

    st.title("Log In")

    login_form = st.form('sharepoint-login-form')

    hawk_id = login_form.text_input("HawkID", key="hawkid-username", placeholder="HawkID@uiowa.edu")

    password = login_form.text_input("HawkID Password", key="hawkid-password", placeholder="HawkID Password",
                                     type="password")

    site_url = login_form.text_input("Sharepoint Site URL", key="sharepoint-url",
                                     placeholder="https://iowa.sharepoint.com/sites/<site-name>/")

    login_button = login_form.form_submit_button("Log in to Sharepoint Site")

    if login_button:
        if not site_url.endswith('/'):
            site_url = site_url + '/'
        cred = {"hawk-id": hawk_id, "password": password, "site-url": site_url}
        if logged_in(cookie_manager, cred):
            time.sleep(0.2)
            cookie_manager.set("cred", cred)
            redirect("/Download%20File")
            return
        login_form.error("Invalid Login Credentials or Sharepoint Site URL")


cookie_manager = get_manager()


time.sleep(.2)


login_form_func()
