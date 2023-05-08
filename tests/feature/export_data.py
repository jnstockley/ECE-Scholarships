"""
UI tests for the export data page
"""
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.usefixtures("login_user")
def click_export_sidebar_link(page: Page):
    """
    clicks the export data link in the sidebar
    """
    export_link = page.get_by_role("link", name="Export Data")
    expect(export_link).to_be_visible()
    export_link.click()
    page.wait_for_load_state("networkidle")

@pytest.mark.usefixtures("login_user")
def test_export_page_visible(page: Page):
    """
    As a user,
    so that I can export data,
    I would like to see an export page tabe on the side bar which I can navigate to
    """
    page.goto("http://localhost:9000/Account", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    click_export_sidebar_link(page)

    export_page_heading = page.get_by_role("heading", name="Export Data").get_by_text(
        "Export Data"
    )
    expect(export_page_heading).to_be_visible()
