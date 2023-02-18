'''
Example Playwright test
'''
import time
from playwright.sync_api import Page, expect

def test_home_page_present(page: Page):
    '''
    As a user, upon opening the app I shall be greeted with a homepage.
    '''
    root_url = "http://localhost:9000"
    # As long as this test runs first it should be the only one requiring this double page load.
    # I think it has something to do with st_pages running on first page visit.
    page.goto(root_url)
    time.sleep(2)
    page.goto(root_url)

    # Expects page to have title Review Application
    expect(page.locator("span", has_text="Review Applicants")).to_have_text("Review sApplicants")
