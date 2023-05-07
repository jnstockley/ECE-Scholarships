"""
Pytest configuration file. Can store fixtures, hooks, and other configuration options.
"""
import time
from dotenv import dotenv_values
from playwright.sync_api import sync_playwright
from scholarship_app.managers.config import ConfigManager

pytest_plugins = ["tests.feature.fixtures.import_data", "tests.feature.fixtures.login"]


def pytest_sessionstart():
    """
    Called at start of testing.
    Our page router has a known issue where the first page load initializes it meaning
    the first visit to our site will show a brief error. By navigating to it we remove this
    error from being encountered in any of our actual tests.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:9000/Account", wait_until="networkidle")
        time.sleep(5)
        browser.close()

    # setup config with default values
    env_config = dotenv_values(".env")
    config = ConfigManager()
    config.set_value("sharepoint_url", env_config["SHAREPOINT_URL"])
