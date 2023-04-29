"""
Global Helper function for functions used with feature tests
"""
import time

from dotenv import dotenv_values
from playwright.sync_api import Page


def login(page: Page):
    """
    Login Function
    """

    config = dotenv_values(".env")

    # Valid Hawk ID
    hawk_id = config["HAWK_ID"]

    # Valid Password
    hawk_id_password = config["HAWK_ID_PASSWORD"]

    # Valid Sharepoint URL
    sharepoint_url = config["SHAREPOINT_URL"]

    page.goto("http://localhost:9000")

    page.wait_for_load_state("networkidle")

    page.goto("http://localhost:9000/Log%20In", wait_until='domcontentloaded')

    hawk_id_textbox = page.get_by_role("textbox", name="HawkID", exact=True)

    password_textbox = page.get_by_role("textbox", name="HawkID Password")

    sharepoint_url_textbox = page.get_by_role("textbox", name="Sharepoint Site URL")

    submit_button_textbox = page.get_by_role("button", name="Log in to Sharepoint Site")

    hawk_id_textbox.click()
    hawk_id_textbox.fill(hawk_id)

    password_textbox.click()
    password_textbox.fill(hawk_id_password)

    sharepoint_url_textbox.click()
    sharepoint_url_textbox.fill(sharepoint_url)

    submit_button_textbox.click()
    # submit_button_textbox.click()

    page.wait_for_load_state("networkidle")

    time.sleep(4)
