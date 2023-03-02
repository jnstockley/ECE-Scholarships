import os

import streamlit as st
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml'))
    return auth


def prepare_flask_request():
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    return {
        'https': 'on',
        'http_host': 'http://localhost:8501',
        'script_name': '/',
        'get_data': '',
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        'lowercase_urlencoding': True,
        'post_data': ''
    }


def redirect(url):
    st.write(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)


params = st.experimental_get_query_params()

if params == {}:

    req = prepare_flask_request()
    auth = init_saml_auth(req)
    if st.button("Login"):
        redirect(auth.login())
elif "uip_ticket" in params and "SAMLRequest" in params:
    print(params)
    redirect("http://localhost:8501")
