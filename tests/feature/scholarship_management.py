'''
Scholarship management tests
'''
from playwright.sync_api import Page, expect

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
    create_btn = page.get_by_role("button", name="Create New Scholarship")

    expect(create_btn).to_have_text('Create New Scholarship')

    create_btn.click()

    expect(page.get_by_text("If certain requirements are N/A, leave them at 0.")).to_be_visible()


def test_edit_button(page: Page):
    '''
    As a user I should be able to edit a preexisting scholarship.
    '''
    page.goto("http://localhost:9000/Scholarship%20Management")
    edit_btn = page.get_by_role("button", name="Edit Existing Scholarship")

    expect(edit_btn).to_have_text('Edit Existing Scholarship')

    edit_btn.click()

    expect(page.get_by_text("Select the scholarship to edit")).to_be_visible()

def test_delete_button(page: Page):
    '''
    As a user I should be able to delete a preexisting scholarship.
    '''
    page.goto("http://localhost:9000/Scholarship%20Management")
    delete_btn = page.get_by_role("button", name="Delete Existing Scholarship")

    expect(delete_btn).to_have_text('Delete Existing Scholarship')

    delete_btn.click()

    expect(page.get_by_text("Select the scholarship to delete")).to_be_visible()

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

# def test_create_scholarship(page: Page):
#     '''
#     As a user, I would like to be able to create a scholarship
#     '''
#     page.goto("http://localhost:9000/Scholarship%20Management", wait_until='domcontentloaded')

#     page.get_by_role("button", name="Create New Scholarship").click()

#     page.get_by_role("textbox", name="Scholarship Name").click()
#     page.get_by_role("textbox", name="Scholarship Name").fill("Test")

#     page.get_by_role("textbox", name="Total amount of Scholarships").click()
#     page.get_by_role("textbox", name="Total amount of Scholarships").fill("500")

#     page.get_by_role("textbox", name="The value of each individual Scholarship").click()
#     page.get_by_role("textbox", name="The value of each individual Scholarship").fill("2000")

#     page.get_by_role("button", name="Create Scholarship").click()

#     expect(page.get_by_text("has been successfully created.")).to_be_visible()

# def test_delete_scholarship(page: Page):
#     '''
#     As a user, I would like to be able to delete a scholarship
#     '''
#     page.goto("http://localhost:9000/Scholarship%20Management", wait_until='domcontentloaded')

#     page.get_by_role("button", name="Delete Existing Scholarship").click()
#     page.get_by_role("selectbox", name="Select the scholarship to delete").select_option('Test')

#     page.get_by_role("button", name="Delete This Scholarship").click()

#     expect(page.get_by_text("Are you sure you want to delete this scholarship? It cannot be undone after.")).to_be_visible()

#     page.get_by_role("button", name="Finalize Deletion").click()

#     expect(page.get_by_text("has been successfully deleted.")).to_be_visible()

# def test_fail_create_scholarship(page: Page):
#     '''
#     As a user so that I cannot try to create an incorrect scholarship,
#     I want it to warn me when I have not filled out the fields
#     '''
#     page.goto("http://localhost:9000/Scholarship%20Management")

#     page.get_by_role("button", name="Create New Scholarship").click()

#     page.get_by_role("textbox", name="Total amount of Scholarships").click()
#     page.get_by_role("textbox", name="Total amount of Scholarships").fill("500")

#     page.get_by_role("textbox", name="The value of each individual Scholarship").click()
#     page.get_by_role("textbox", name="The value of each individual Scholarship").fill("2000")

#     create_sch_btn = page.get_by_role("button", name="Create Scholarship")

#     expect(create_sch_btn).to_have_text('Create Scholarship')

#     create_sch_btn.click()

#     expect(page.get_by_text("Please make sure all the fields are filled out.")).to_be_visible()

def test_import_page(page: Page):
    '''
    As a user I should be able to see the import data section
    of scholarship management
    '''
    page.goto("http://localhost:9000/Scholarship%20Management", wait_until='domcontentloaded')

    import_heading = page.get_by_role("heading", name="Import Scholarships").get_by_text("Import Scholarships")

    expect(import_heading).to_have_text('Import Scholarships')

def test_browse_button(page: Page):
    '''
    As a user I should be able to create a new scholarship.
    '''
    page.goto("http://localhost:9000/Scholarship%20Management", wait_until='domcontentloaded')
    browse_btn = page.get_by_role("button", name="Browse files")

    expect(browse_btn).to_have_text('Browse files')
