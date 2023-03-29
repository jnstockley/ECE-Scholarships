'''
UI tests for the export data page
'''
from playwright.sync_api import Page, expect
import pytest

def click_export_sidebar_link(page: Page):
    '''
    clicks the export data link in the sidebar
    '''
    export_link = page.get_by_role("link", name="Export Data")
    expect(export_link).to_be_visible()
    export_link.click()
    page.wait_for_load_state("networkidle")

def test_export_page_visible(page: Page):
    '''
    As a user,
    so that I can export data,
    I would like to see an export page tabe on the side bar which I can navigate to
    '''
    page.goto("http://localhost:9000")
    click_export_sidebar_link(page)

    export_page_heading = page.get_by_role("heading", name="Export Data").get_by_text("Export Data")
    expect(export_page_heading).to_be_visible()

def test_export_page_with_no_data_imported(page: Page):
    '''
    As a user,
    when navigating the the export data page,
    I would like it to be apparent that there is no data to export.
    '''
    page.goto("http://localhost:9000/Export Data")
    expect(page.get_by_text("Once you've imported data you can return to this page to export it the combined excel sheet")).to_be_visible()

@pytest.mark.usefixtures("skip_all_similar_import_complete_page")
def test_export_page_with_imported(skip_all_similar_import_complete_page: Page):
    '''
    As a user,
    when navigating the the export data page,
    I would like to be able to export my imported data
    '''
    # shorten name of variable
    page = skip_all_similar_import_complete_page
    click_export_sidebar_link(page)

    expect(page.get_by_text("Download your merged data locally")).to_be_visible()
    page.get_by_role("link", name="Export Data").click()
    with page.expect_download() as _download_info:
        with page.expect_popup() as _page1_info:
            page.get_by_role("button", name="Export").click()
