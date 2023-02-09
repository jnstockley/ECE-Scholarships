from playwright.sync_api import Page, expect


def test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(page: Page):
    ROOT_URL = "http://localhost:8501"
    page.goto(ROOT_URL)

    # Expects title of home page to be `home . Streamlit`
    expect(page).to_have_title("home · Streamlit")

    # create a locator for the `about` page
    about = page.get_by_role("link", name="About")

    # Expects the link to direct to the about page
    expect(about).to_have_attribute("href", f"{ROOT_URL}/about")

    # Click the about link.
    about.click()

    # Expects the page to have a heading titled `Example about page`
    expect(page.get_by_role("heading", name="Example about page")).to_be_visible()
