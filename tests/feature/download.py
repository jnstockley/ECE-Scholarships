import time

from playwright.sync_api import Page, expect

from tests.feature.login import login


def test_download_page(page: Page):
    """
    Tests that the download page exists, and has the correct title
    """
    page.goto("http://localhost:9000", wait_until='domcontentloaded')

    time.sleep(2)

    login(page)

    download_page_link = page.get_by_role("link", name="Download File")

    expect(download_page_link).to_have_text("Download File")

    download_page_link.click()

    download_page_heading = page.get_by_role("heading", name="Download A File")
    expect(download_page_heading).to_have_text("Download A File")


def test_download_valid_file(page: Page):
    page.goto("http://localhost:9000", wait_until='domcontentloaded')

    time.sleep(2)

    login(page)

    page.goto("http://localhost:9000/Download%20File", wait_until='domcontentloaded')

    file_download_dropdown = page.locator('//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[5]/div[1]/div/div[1]/div/div/div/div[1]')

    expect(file_download_dropdown).to_have_text("Select File")

    file_download_dropdown.click()

    file = page.locator('//*[@id="bui8__anchor"]/div/div')

    file.click()

    file_name = file.text_content()

    download_button = page.get_by_role("button", name="Download File")

    expect(download_button).to_have_text("Download File")

    download_button.click()

    success_message = page.locator('//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[5]/div[1]/div/div[3]')

    expect(success_message).to_have_text(f"Downloaded {file_name}")


def test_download_invalid_file(page: Page):
    page.goto("http://localhost:9000", wait_until='domcontentloaded')

    time.sleep(2)

    login(page)

    page.goto("http://localhost:9000/Download%20File", wait_until='domcontentloaded')

    file_download_dropdown = page.locator(
        '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[5]/div[1]/div/div[1]/div/div/div/div[1]')

    expect(file_download_dropdown).to_have_text("Select File")

    download_button = page.get_by_role("button", name="Download File")

    expect(download_button).to_have_text("Download File")

    download_button.click()

    error_message = page.locator('//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[5]/div[1]/div/div[3]/div/div')

    expect(error_message).to_have_text("Invalid File Selected")
