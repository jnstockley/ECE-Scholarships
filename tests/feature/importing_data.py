'''
Test functionality of the import document tools.
'''
from playwright.sync_api import Page
#HELPERS:
def goto_import(_page: Page):
    '''
    This function will take your session to the import page
    '''

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

def test_import_button(_page: Page):
    '''
    As a user I should be able to click import once I have added a file.
    '''
    # goto import page
    # click on add file
