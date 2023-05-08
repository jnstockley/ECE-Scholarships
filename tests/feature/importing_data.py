# pylint: disable=R0801
"""
Test functionality of the import document tools.
"""
import os
import pytest
from playwright.sync_api import Page, expect

ABSOLUTE_PATH = os.path.dirname(__file__)
SAMPLE_FILE_PATHS = [
    os.path.join(ABSOLUTE_PATH, "../data/ece_scholarship_applicants.xlsx"),
    os.path.join(ABSOLUTE_PATH, "../data/ece_school_applicants.xlsx"),
]


@pytest.mark.usefixtures("login_user")
def test_import_page(page: Page):
    """
    As a user I should be able to find and navigate to
    the import data page.
    """
    page.goto("http://localhost:9000", wait_until="domcontentloaded")
    import_data_link = page.get_by_role("link", name="Import Data")

    expect(import_data_link).to_have_text("Import Data")

    import_data_link.click()
    import_data_heading = page.get_by_role("heading", name="Import Data").get_by_text(
        "Import Data"
    )

    expect(import_data_heading).to_have_text("Import Data")


@pytest.mark.usefixtures("login_user")
def test_add_file_button(page: Page):
    """
    As a user I should be able to add files I can import
    to the application
    """
    page.goto("http://localhost:9000/Import%20Data")
    add_files_btn = page.get_by_role("button", name="Browse files")

    # The page should have a browse files button
    expect(add_files_btn).to_have_text("Browse files")


@pytest.mark.usefixtures("login_user")
@pytest.mark.usefixtures("skip_all_similar_import_complete_page")
def test_import_files_start_to_end(skip_all_similar_import_complete_page: Page):
    """
    As a user so that I can upload scholarship applications details from multiple sources,
    I would like to be able to upload several excel files and combine them across a single
    common column with unique values.

    This test verifies the entire import data flow is functioning
    """
    skip_all_similar_import_complete_page.get_by_role(
        "button", name="import another"
    ).click()
    expect(
        skip_all_similar_import_complete_page.get_by_role("heading", name="Import Data")
    ).to_have_text("Import Data")


@pytest.mark.usefixtures("login_user")
@pytest.mark.usefixtures("merge_all_similar_import_complete_page")
def test_import_files_start_to_end_with_merging(
    merge_all_similar_import_complete_page: Page,
):
    """
    As a user so that I can upload scholarship applications details from multiple sources,
    I would like to be able to upload several excel files and combine them across a single
    common column with unique values.

    With merging specifies that the user chooses to merge all similar columns instead of skip!
    """
    merge_all_similar_import_complete_page.get_by_role(
        "button", name="import another"
    ).click()
    expect(
        merge_all_similar_import_complete_page.get_by_role(
            "heading", name="Import Data"
        )
    ).to_have_text("Import Data")


@pytest.mark.usefixtures("login_user")
def test_import_files_with_no_files_selected(page: Page):
    """
    As a user so that I can understand how to use the application, I would like to be notified
    when no files have been selected for import.
    """
    page.goto("http://localhost:9000/Import%20Data", wait_until="domcontentloaded")

    page.get_by_role("button", name="Import").click()

    expect(page.get_by_text("No files selected!")).to_be_visible()


@pytest.mark.usefixtures("login_user")
def test_import_files_with_no_final_alignment_name(page: Page):
    """
    As a user so that I can understand how to use the application, I would like to be notified
    when no files have been selected for import.
    """
    page.goto("http://localhost:9000/Import%20Data", wait_until="domcontentloaded")

    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Browse files").click()
    file_chooser = fc_info.value
    file_chooser.set_files(SAMPLE_FILE_PATHS)

    page.get_by_role("button", name="Import").click()
    expect(page.get_by_text("Select Alignment Columns")).to_have_text(
        "Select Alignment Columns"
    )

    page.get_by_role(
        "combobox", name="Selected Category. ece_scholarship_applicants.xlsx"
    ).click()
    page.get_by_text("UID").click()
    page.get_by_role(
        "combobox", name="Selected Decision_Date. ece_school_applicants.xlsx"
    ).click()
    page.get_by_text("UID.1").click()

    page.get_by_role("button", name="submit").click()

    expect(
        page.get_by_text(
            "Error: please specify your final combined alignment column name"
        )
    ).to_be_visible()


@pytest.mark.usefixtures("login_user")
@pytest.mark.usefixtures("import_similar_column_page")
def test_merge_similar_columns_script_editor(page: Page):
    """
    As a user so that I can specify my own merge technique with a high level of control,
    I'd like to be able to write my own merge function for the similar columns in Python.
    """
    expect(
        page.get_by_role("button", name="Create Custom Merge Script (ADVANCED)")
    ).to_be_visible()

    page.get_by_role("button", name="Create Custom Merge Script (ADVANCED)").click()

    expect(page.get_by_text("Make changes to the function")).to_be_visible()
