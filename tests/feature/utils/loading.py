'''
Utilities for assisting with streamlit page loading events.
'''
from playwright.sync_api import Page, expect

def wait_for_streamlit_loading_complete(page: Page):
    '''
    Waits until the streamlit loading animation is gone.
    '''
    expect(page.get_by_text("Running...Stop")).not_to_be_visible()
