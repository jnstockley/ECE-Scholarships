"""
Scholarship management tests
"""
import pytest
from playwright.sync_api import Page, expect


# TESTS:
@pytest.mark.usefixtures("login_user")
def test_scholarship_page(page: Page):
    """
    As a user I should be able to find and navigate to
    the scholarship management page
    """

    page.goto("http://localhost:9000")
    scholarship_link = page.get_by_role("link", name="Scholarship Management")

    expect(scholarship_link).to_have_text('Scholarship Management')

    scholarship_link.click()
    scholarship_heading = page.get_by_role("heading", name="Scholarship Management").get_by_text(
        "Scholarship Management")

    page.wait_for_load_state("networkidle")

    expect(scholarship_heading).to_have_text('Scholarship Management')


@pytest.mark.usefixtures("login_user")
def test_create_button(page: Page):
    """
    As a user I should be able to create a new scholarship.
    """
    page.goto("http://localhost:9000/Scholarship%20Management")
    create_btn = page.get_by_role("button", name="Create New Scholarship")

    expect(create_btn).to_have_text('Create New Scholarship')

    create_btn.click()

    expect(page.get_by_text("If certain requirements are N/A, leave them at 0.")).to_be_visible()


@pytest.mark.usefixtures("login_user")
def test_edit_button(page: Page):
    """
    As a user I should be able to edit a preexisting scholarship.
    """
    page.goto("http://localhost:9000/Scholarship%20Management")
    edit_btn = page.get_by_role("button", name="Edit Existing Scholarship")

    expect(edit_btn).to_have_text('Edit Existing Scholarship')

    edit_btn.click()

    expect(page.get_by_text("Select the scholarship to edit")).to_be_visible()


@pytest.mark.usefixtures("login_user")
def test_delete_button(page: Page):
    """
    As a user I should be able to delete a preexisting scholarship.
    """
    page.goto("http://localhost:9000/Scholarship%20Management")
    delete_btn = page.get_by_role("button", name="Delete Existing Scholarship")

    expect(delete_btn).to_have_text('Delete Existing Scholarship')

    delete_btn.click()

    expect(page.get_by_text("Select the scholarship to delete")).to_be_visible()


@pytest.mark.usefixtures("login_user")
def test_edit_scholarship(page: Page):
    """
    As a user so that edit preexisting scholarships,
    I would like to be able to go through a series of steps to edit a scholarship
    """
    page.goto("http://localhost:9000/Scholarship%20Management", wait_until='domcontentloaded')

    page.get_by_role("button", name="Edit Existing Scholarship").click()
    page.get_by_role("button", name="Edit This Scholarship").click()
    page.get_by_role("button", name="Finalize Changes").click()

    expect(page.get_by_text("has been successfully edited.")).to_be_visible()


@pytest.mark.usefixtures("login_user")
def test_import_page(page: Page):
    """
    As a user I should be able to see the import data section
    of scholarship management
    """
    page.goto("http://localhost:9000/Scholarship%20Management", wait_until='domcontentloaded')

    import_heading = page.get_by_role("heading", name="Import Scholarships").get_by_text("Import Scholarships")

    expect(import_heading).to_have_text('Import Scholarships')
