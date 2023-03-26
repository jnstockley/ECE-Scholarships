"""
Signs the user into SharePoint
"""
import re
import time
from re import Pattern

import streamlit as st
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext

from utils.cookies import get_manager

HAWKID_REGEX = re.compile(r"[a-zA-Z]{1}[a-zA-Z0-9]{2,}@uiowa.edu")

PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]?)[A-Za-z\d@$!%*#?&]{8,}$")

SITE_URL_REGEX = re.compile(r"https://iowa.sharepoint.com/sites/.+")


def regex_validation(string: str, regex: Pattern[str]) -> bool | None:
    """
    Validates regex, used to check sign in creds before connecting to sharepoint
    :param string: String to match
    :param regex: Regex used to match against the string
    :return: True if matches, otherwise none
    """
    return re.fullmatch(regex, string)


def sharepoint_login(hawk_id: str, password: str, site_url: str):
    """
    Makes the first connection to sharepoint and ensure the connection was successful
    :param hawk_id: Username
    :param password: Password
    :param site_url: Sharepoint Site URL
    :return: True if connected, otherwise false
    """
    with st.spinner("Logging into Sharepoint..."):
        creds = ClientContext(site_url).with_credentials(UserCredential(hawk_id, password))
        try:
            web = creds.web.get().execute_query()
        except IndexError:
            return False
        except ClientRequestException:
            return False
        return f"{web.url}/" == site_url


def validate_and_login(hawk_id: str, password: str, site_url: str, login_form):
    """
    Basic Checking of login creds using regex
    :param hawk_id: Username
    :param password: Password
    :param site_url: Sharepoint Site URL
    :param login_form: Login form, used to give error messages
    :return: True if valid, otherwise false
    """
    if regex_validation(hawk_id, HAWKID_REGEX) and regex_validation(password, PASSWORD_REGEX) \
            and regex_validation(site_url, SITE_URL_REGEX) and sharepoint_login(hawk_id, password, site_url):
        login_form.success("Logged In")
        return True
    login_form.error("Invalid Login Credentials or Sharepoint Site URL")
    return False


def login_form_func():
    """
    Sets up the login and connection form
    :return:
    """
    login_form = st.form('sharepoint-login-form')

    hawk_id = login_form.text_input("HawkID", key="hawkid-username", placeholder="HawkID@uiowa.edu")

    password = login_form.text_input("HawkID Password", key="hawkid-password", placeholder="HawkID Password",
                                     type="password")

    site_url = login_form.text_input("Sharepoint Site URL", key="sharepoint-url",
                                     placeholder="https://iowa.sharepoint.com/sites/<site-name>/")

    login_button = login_form.form_submit_button("Log in to Sharepoint Site")

    if login_button:
        if validate_and_login(hawk_id, password, site_url, login_form):
            cookie_manager.set("cred", {"hawk-id": hawk_id, "password": password, "site-url": site_url})


cookie_manager = get_manager()


time.sleep(.2)


login_form_func()
