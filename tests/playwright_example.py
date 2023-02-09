'''
Example Playwright test
'''
from playwright.sync_api import Page, expect


def playwright_test(page: Page):
    '''
    Example playwright test
    :param page:
    :return:
    '''
    root_url = "http://localhost:8501"
    page.goto(root_url)

    # Expects title of home page to be `home . Streamlit`
    expect(page).to_have_title("home · Streamlit")

    # create a locator for the `about` page
    about = page.get_by_role("link", name="About")

    # Expects the link to direct to the about page
    expect(about).to_have_attribute("href", f"{root_url}/about")

    # Click the about link.
    about.click()

    # Expects the page to have a heading titled `Example about page`
    expect(page.get_by_role("heading", name="Example about page")).to_be_visible()
