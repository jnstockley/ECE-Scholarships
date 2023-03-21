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