# pylint: disable=W0621
'''
Fixtures for assisting with imported data routines
'''
import os
import re
import pytest
from playwright.sync_api import Page, expect

ABSOLUTE_PATH = os.path.dirname(__file__)
SAMPLE_FILE_PATHS = [os.path.join(ABSOLUTE_PATH, '../../data/ece_scholarship_applicants.xlsx'), os.path.join(ABSOLUTE_PATH, '../../data/ece_school_applicants.xlsx')]

# File uploader with streamlit not working on chromium
@pytest.mark.skip_browser("chromium")
@pytest.fixture
def import_similar_column_page(page: Page) -> Page:
    '''
    Fixure which takes you to the point in the import data flow where you are
    on the similar column merge page (if any similar columns are detected)
    '''
    page.goto("http://localhost:9000/Import%20Data", wait_until='domcontentloaded')

    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Browse files").click()
    file_chooser = fc_info.value
    file_chooser.set_files(SAMPLE_FILE_PATHS)

    page.get_by_role("button", name="Import").click()
    expect(page.get_by_text("Select Alignment Columns")).to_have_text("Select Alignment Columns")

    page.get_by_role("combobox", name="Selected Category. ece_scholarship_applicants.xlsx").click()
    page.get_by_text("UID").click()
    page.get_by_role("combobox", name="Selected Decision_Date. ece_school_applicants.xlsx").click()
    page.get_by_text("UID.1").click()

    page.get_by_role("textbox", name="Final column name:").click()
    page.get_by_role("textbox", name="Final column name:").fill("UID")

    page.get_by_role("button", name="submit").click()

    expect(page.get_by_text("Duplicate Column(s) Found")).to_have_text("Duplicate Column(s) Found")

    page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Next").click()

    return page

def handle_similar_columns(page: Page, press_option:str = "skip"):
    '''
    Handles interacting with the similar column UI. Will press the button
    corresponding to the press_option parameter until there are no similar
    columns remaining.

    Parameters
    ----------
    press_option : str, optional
    '''
    expect(page.get_by_text('Similar Columns Have Been Detected')).to_be_visible(timeout=20000)

    remaining_label = page.get_by_role('paragraph').filter(has_text=re.compile(".+ remaining..."))
    remaining_count = int(remaining_label.inner_text().replace(" remaining...", ""))
    # Keep clicking skip until we have reached the end
    for i in range(remaining_count + 1, -1, -1):
        page.get_by_role("button", name=press_option).click()
        if not i == 0:
            # Click the upcomming remaining index as a quick method to tell when streamlit has finished re-rendering the page
            page.get_by_text(f"{i-1} remaining...").click()

@pytest.fixture
def skip_all_similar_import_complete_page(import_similar_column_page: Page) -> Page:
    '''
    Page fixture where the user has completed the import data flow and chose to skip
    merging all similar columns.
    '''
    handle_similar_columns(import_similar_column_page)
    expect(import_similar_column_page.get_by_text("import completed!")).to_have_text("import completed!")
    return import_similar_column_page

@pytest.fixture
def merge_all_similar_import_complete_page(import_similar_column_page: Page) -> Page:
    '''
    Page fixture where the user has completed the import data flow and chose to skip
    merging all similar columns.
    '''
    handle_similar_columns(import_similar_column_page)
    expect(import_similar_column_page.get_by_text("import completed!")).to_have_text("import completed!")
    return import_similar_column_page
