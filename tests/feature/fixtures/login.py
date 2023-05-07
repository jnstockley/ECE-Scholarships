"""
Fixtures for handling the logged-in user.
"""
import time

import pytest
from dotenv import dotenv_values
from playwright.sync_api import Page

CONFIG = dotenv_values(".env")
TEST_HAWK_ID = CONFIG["HAWK_ID"]
TEST_HAWK_ID_PASSWORD = CONFIG["HAWK_ID_PASSWORD"]
TEST_SHAREPOINT_URL = CONFIG["SHAREPOINT_URL"]


@pytest.fixture
def login_user(page: Page) -> Page:
    """
    Logins in a valid user account to the test session.
    """
    page.goto("http://localhost:9000", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    page.goto("http://localhost:9000/Account", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")

    hawk_id_textbox = page.get_by_role("textbox", name="HawkID", exact=True)
    password_textbox = page.get_by_role("textbox", name="HawkID Password")

    submit_button_textbox = page.get_by_role("button", name="Log in to Sharepoint Site")

    hawk_id_textbox.fill(TEST_HAWK_ID)
    password_textbox.fill(TEST_HAWK_ID_PASSWORD)

    # Fixes weird issue where clicking the button after filling form causes button click to be missed
    # It is streamlit related
    page.get_by_text("Log In", exact=True).click(delay=1000)

    submit_button_textbox.click()

    page.wait_for_load_state("networkidle")
    time.sleep(4)

    return page
