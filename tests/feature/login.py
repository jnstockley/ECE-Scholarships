"""
Login Feature Test
"""
import pytest
from playwright.sync_api import Page, expect


def test_login_page(page: Page):
    """
    Tests that the login page exists, and has the correct title
    """
    page.goto("http://localhost:9000", wait_until='domcontentloaded')

    page.wait_for_load_state("networkidle")

    login_page_link = page.get_by_role("link", name="Log In")

    expect(login_page_link).to_have_text("Log In")

    login_page_link.click(delay=500)

    page.wait_for_load_state("networkidle")

    login_page_heading = page.get_by_role("heading", name="Log In").get_by_text("Log In")
    expect(login_page_heading).to_have_text("Log In")


def test_invalid_login_creds(page: Page):
    """
    Tests that the login page doesn't connect to sharepoint using invalid login details
    """
    page.goto("http://localhost:9000/Log%20In", wait_until='domcontentloaded')

    page.wait_for_load_state("networkidle")

    # Invalid Hawk ID
    invalid_hawk_id = "test"

    # Invalid Password
    invalid_password = "1234"

    # Invalid Sharepoint URL
    invalid_sharepoint_url = "https://iowa.sharepoint.com/sites"

    hawk_id_textbox = page.get_by_role("textbox", name="HawkID", exact=True)
    password_textbox = page.get_by_role("textbox", name="HawkID Password")
    sharepoint_url_textbox = page.get_by_role("textbox", name="Sharepoint Site URL")
    submit_button_textbox = page.get_by_role("button", name="Log in to Sharepoint Site")

    hawk_id_textbox.type(invalid_hawk_id)
    password_textbox.fill(invalid_password)
    sharepoint_url_textbox.fill(invalid_sharepoint_url)

    submit_button_textbox.click(delay=500)

    page.wait_for_load_state("networkidle")

    expect(page.get_by_text("Invalid Login Credentials or Sharepoint Site URL")).to_be_visible()


@pytest.mark.usefixtures("login_user")
def test_valid_login_creds(page: Page):
    """
    Tests that the login pages connects to the sharepoint site using valid credentials
    Also checks that download page responds correctly to being logged in
    """
    page.goto("http://localhost:9000/Download%20File", wait_until='domcontentloaded')

    page.wait_for_load_state("networkidle")

    download_file_page_heading = page.get_by_role("heading", name="Download A File").get_by_text("Download A File")

    expect(download_file_page_heading).to_have_text("Download A File")
