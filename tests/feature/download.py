"""
Feature test for downloading files from SharePoint
"""
import time

from playwright.sync_api import Page, expect

from tests.feature import hawk_id_login


def test_download_page(page: Page):
    """
    Tests that the download page exists, and has the correct title
    """
    hawk_id_login(page)

    download_page_link = page.get_by_role("link", name="Download File")

    expect(download_page_link).to_have_text("Download File")

    download_page_link.click()

    download_page_heading = page.get_by_role("heading", name="Download A File")
    expect(download_page_heading).to_have_text("Download A File")


def test_download_valid_file(page: Page):
    """
    Tests downloading a valid file from SharePoint
    """
    hawk_id_login(page)

    page.goto("http://localhost:9000/Download%20File", wait_until='domcontentloaded')

    page.wait_for_load_state("networkidle")

    file_download_dropdown = page.get_by_text("Select File")
    # page.locator('//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[1]')

    # expect(file_download_dropdown).to_have_text("Select File")

    file_download_dropdown.click()

    file = page.locator('//*[@id="bui8__anchor"]/div/div')

    file.click()

    # file_name = file.text_content()

    download_button = page.get_by_role("button", name="Download File")

    expect(download_button).to_have_text("Download File")

    download_button.click()

    page.wait_for_load_state("networkidle")

    success_message = page.get_by_text("Downloaded")

    expect(success_message).to_be_visible()


def test_download_invalid_file(page: Page):
    """
    Tests downloading a valid file from SharePoint
    """
    hawk_id_login(page)

    page.goto("http://localhost:9000/Download%20File", wait_until='domcontentloaded')

    page.wait_for_load_state("networkidle")

    download_button = page.get_by_role("button", name="Download File")

    expect(download_button).to_have_text("Download File")

    download_button.click()

    page.wait_for_load_state("networkidle")

    error_message = page.get_by_text("Invalid File Selected")

    expect(error_message).to_have_text("Invalid File Selected")