'''
Test functionality of the import document tools.
'''
import os
import time
from playwright.sync_api import Page, expect

# TESTS:
def test_import_page(page: Page):
    '''
    As a user I should be able to find and navigate to
    the import data page.
    '''
    page.goto("http://localhost:9000")
    import_data_link = page.get_by_role("link", name="Import Data")

    expect(import_data_link).to_have_text('Import Data')

    import_data_link.click()
    import_data_heading = page.get_by_role("heading", name="Import Data").get_by_text("Import Data")

    expect(import_data_heading).to_have_text('Import Data')

def test_add_file_button(page: Page):
    '''
    As a user I should be able to add files I can import
    to the application
    '''
    page.goto("http://localhost:9000/Import%20Data")
    add_files_btn = page.get_by_role("button", name="Browse files")

    # The page should have a browse files button
    expect(add_files_btn).to_have_text('Browse files')
