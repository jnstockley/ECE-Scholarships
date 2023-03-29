'''
UI tests for the export data page
'''
from playwright.sync_api import Page, expect
import pytest

def export_page_visible(page: Page):
    '''
    As a user,
    so that I can export data,
    I would like to see an export page tabe on the side bar which I can navigate to
    '''
    page.goto("http://localhost:9000")
    export_link = page.get_by_role("link", name="Export Data")
    expect(export_link).to_be_visible()
    export_link.click()

    export_page_heading = page.get_by_role("heading", name="Export Data").get_by_text("Export Data")
    expect(export_page_heading).to_be_visible()

def export_page_with_no_data_imported(page: Page):
    '''
    As a user,
    when navigating the the export data page,
    I would like it to be apparent that there is no data to export.
    '''
    page.goto("http://localhost:9000/Export Data")
    expect(page.get_by_Text("Once you've imported data you can return to this page to export it the combined excel sheet")).to_be_visible()

@pytest.mark.usefixtures("skip_all_similar_import_complete_page")
def export_page_with_imported(skip_all_similar_import_complete_page: Page):
    '''
    As a user,
    when navigating the the export data page,
    I would like to be able to export my imported data
    '''
    # shorten name of variable
    page = skip_all_similar_import_complete_page
    page.goto("http://localhost:9000/Export Data")

    expect(page.get_by_Text("Download your merged data locally")).to_be_visible()
    expect(page.get_attribute('button', name='Export')).to_be_visible()
