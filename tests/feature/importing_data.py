'''
Test functionality of the import document tools.
'''
import os
import time
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

def test_other(page: Page):
    page.goto('https://imagecompressor.com/')

    #await page.set_content("<input type=file>")
    with page.expect_file_chooser(timeout=5000) as fc_info:
        print('other')
        page.get_by_text("Upload Files", exact=True).click()
        print('click2')
    print('bleep boop')
    file_chooser = fc_info.value
    assert file_chooser
    print('test')

def test_add_files(page: Page):
    '''
    As a user I should be able to add files to import
    '''
    page.goto("http://localhost:9000/Import%20Data")
    add_files_btn = page.get_by_role("button", name="Browse files")

    # The page should have a browse files button
    expect(add_files_btn).to_have_text('Browse files')

    #add_files_btn.set_input_files([os.path.join(os.getcwd(), 'tests/data/ece_scholarship_applicants.xlsx')])
    with page.expect_file_chooser(timeout=10000) as fc_info:
        print('event')
        page.get_by_role("button", name="Browse files").click()
        page.get_by_role("button", name="Browse files").click()
        print('click1')
    file_chooser = fc_info.value
    print('hello')
    #file_chooser.set_files(os.path.join(os.getcwd(), 'tests/data/ece_scholarship_applicants.xlsx'))

    assert file_chooser