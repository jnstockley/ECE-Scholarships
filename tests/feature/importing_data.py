'''
Test functionality of the import document tools.
'''
import os
from playwright.sync_api import Page, expect

# TESTS:
def test_import_page(_page: Page):
    '''
    As a user I should be able to find and navigate to
    the import data page.
    '''
    # Check that sidebar has "Import"
    # Click on that sidebar element
    # Check that title on page has "Import Data"

def test_add_file_button(_page: Page):
    '''
    As a user I should be able to add files I can import
    to the application
    '''
    # goto import page
    # Click on add file



def test_add_files(page: Page):
    '''
    As a user I should be able to add files to import
    '''
    page.goto("http://localhost:9000/Import%20Data")
    add_files_btn = page.get_by_role("button", name="Browse files")

    # The page should have a browse files button
    expect(add_files_btn).to_have_text('Browse files')

    #add_files_btn.set_input_files([os.path.join(os.getcwd(), 'tests/data/ece_scholarship_applicants.xlsx')])
    add_files_btn.click()

    file_chooser = page.wait_for_event('filechooser')

    file_chooser.set_files(os.path.join(os.getcwd(), 'tests/data/ece_scholarship_applicants.xlsx'))
