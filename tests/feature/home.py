"""
Tests that the home page exists, and respects user sign in
"""
from playwright.sync_api import Page, expect

from tests.feature.login import login


def test_home_page_exists(page: Page):
    """
    Tests that the home page exists
    """
    page.goto("http://localhost:9000", wait_until='domcontentloaded')
    home_page_link = page.get_by_role("link", name="Home")

    expect(home_page_link).to_have_text("Home")


def test_home_page_not_logged_in(page: Page):
    """
    Tests that the home page redirects to log in page if not signed in
    """
    page.goto("http://localhost:9000", wait_until='domcontentloaded')

    page_title = page.get_by_role("heading")
    expect(page_title).to_have_text("Log In")

def test_home_page_logged_in(page: Page):
    """
    Tests that the home page doesn't redirect if the user is signed in
    """
    login(page)

    page.goto("http://localhost:9000", wait_until='domcontentloaded')

    home_page_heading = page.get_by_role("heading", name="Home").get_by_text("Home")
    expect(home_page_heading).to_have_text("Home")
