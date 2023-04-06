import os
import time

from playwright.sync_api import Page, expect


def test_home_page_exists(page: Page):
    page.goto("http://localhost:9000", wait_until='domcontentloaded')
    home_page_link = page.get_by_role("link", name="Home")

    expect(home_page_link).to_have_text("Home")


def test_home_page_not_logged_in(page: Page):
    page.goto("http://localhost:9000", wait_until='domcontentloaded')

    page_title = page.get_by_role("heading")
    expect(page_title).to_have_text("Log In")


def test_home_page_logged_in(page: Page):
    # Valid Hawk ID
    hawk_id = os.getenv("HAWK_ID")

    # Valid Password
    hawk_id_password = os.getenv("HAWK_ID_PASSWORD")

    # Valid Sharepoint URL
    sharepoint_url = os.getenv("SHAREPOINT_URL")

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

    time.sleep(4)

    page.goto("http://localhost:9000", wait_until='domcontentloaded')

    home_page_heading = page.get_by_role("heading", name="Home").get_by_text("Home")
    expect(home_page_heading).to_have_text("Home")