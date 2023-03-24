import os
from playwright.sync_api import Page, expect

ABSOLUTE_PATH = os.path.dirname(__file__)
SAMPLE_FILE_PATHS = [os.path.join(ABSOLUTE_PATH, '../data/ece_scholarship_applicants.xlsx'), os.path.join(ABSOLUTE_PATH, '../data/ece_school_applicants.xlsx')]

# TESTS:
def test_scholarship_page(page: Page):
    '''
    As a user I should be able to find and navigate to
    the scholarship management page
    '''
    page.goto("http://localhost:9000")
    scholarship_link = page.get_by_role("link", name="Scholarship Management")

    expect(scholarship_link).to_have_text('Scholarship Management')

    scholarship_link.click()
    scholarship_heading = page.get_by_role("heading", name="Scholarship Management").get_by_text("Scholarship Management")

    expect(scholarship_heading).to_have_text('Scholarship Management')

def test_create_button(page: Page):
    '''
    As a user I should be able to create a new scholarship.
    '''
    page.goto("http://localhost:9000/Scholarship%20Management")
    add_files_btn = page.get_by_role("button", name="Create New Scholarship")
    
    expect(add_files_btn).to_have_text('Create New Scholarship')

def test_edit_button(page: Page):
    '''
    As a user I should be able to edit a preexisting scholarship.
    '''
    page.goto("http://localhost:9000/Scholarship%20Management")
    add_files_btn = page.get_by_role("button", name="Edit Existing Scholarship")
    
    expect(add_files_btn).to_have_text('Edit Existing Scholarship')

def test_delete_button(page: Page):
    '''
    As a user I should be able to delete a preexisting scholarship.
    '''
    page.goto("http://localhost:9000/Scholarship%20Management")
    add_files_btn = page.get_by_role("button", name="Delete Existing Scholarship")
    
    expect(add_files_btn).to_have_text('Delete Existing Scholarship')

def test_edit_scholarship(page: Page):
    '''
    As a user so that edit preexisting scholarships, 
    I would like to be able to go through a series of steps to edit a scholarship
    '''
    page.goto("http://localhost:9000/Scholarship%20Management", wait_until='domcontentloaded')

    page.get_by_role("button", name="Edit Existing Scholarship").click()
    page.get_by_role("button", name="Edit This Scholarship").click()
    page.get_by_role("button", name="Finalize Changes").click()

    expect(page.get_by_text("has been successfully edited.")).to_be_visible()