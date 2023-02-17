'''
Example Playwright test
'''
from playwright.sync_api import Page, expect

def test_home_page_present(page: Page):
    '''
    As a user, upon opening the app I shall be greeted with a homepage.
    '''
    root_url = "http://localhost:9000"
    page.goto(root_url)

    # Expects title of home page to be `home . Streamlit`
    expect(page).to_have_title("home · Streamlit")
