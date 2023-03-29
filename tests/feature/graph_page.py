'''
Test functionality of the graphs standalone page
'''
from playwright.sync_api import Page, expect

def test_graph_page(page: Page):
    '''
    Test graph page visible
    '''
    page.goto("http://localhost:9000")
    metrics_link = page.get_by_role("link", name="Student Metrics")

    expect(metrics_link).to_have_text('Student Metrics')

    metrics_link.click()
    metric_data_heading = page.get_by_role("heading", name="Student Metrics").get_by_text("Student Metrics")

    expect(metric_data_heading).to_have_text("Student Metrics")

def test_student_selectbox(page: Page):
    '''
    Test student selectbox working
    '''
    page.goto("http://localhost:9000/Student Metrics")
    page.locator("div").filter(has_text="Leyla Hair").first.is_visible()
