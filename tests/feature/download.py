"""
Feature test for downloading files from SharePoint
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.usefixtures("login_user")
def test_download_page(page: Page):
    """
    Tests that the download page exists, and has the correct title
    """
    page.goto("http://localhost:9000/Download%20File", wait_until="domcontentloaded")

    page.wait_for_load_state("networkidle")

    download_page_link = page.get_by_role("link", name="Download File")

    expect(download_page_link).to_have_text("Download File")

    download_page_link.click()

    page.wait_for_load_state("networkidle")

    download_page_heading = page.get_by_role("heading", name="Download A File")
    expect(download_page_heading).to_have_text("Download A File")


@pytest.mark.usefixtures("login_user")
def test_download_invalid_file(page: Page):
    """
    Tests downloading a valid file from SharePoint
    """
    page.goto("http://localhost:9000/Download%20File", wait_until="domcontentloaded")

    page.wait_for_load_state("networkidle")

    download_button = page.get_by_role("button", name="Download File")

    expect(download_button).to_have_text("Download File")

    download_button.click()

    page.wait_for_load_state("networkidle")

    error_message = page.get_by_text("Invalid File Selected")

    expect(error_message).to_have_text("Invalid File Selected")
