'''
Test functionality of the graphs standalone page
'''
from playwright.sync_api import Page, expect

def test_graph_page(page: Page):
    '''
    '''
    page.goto("http://localhost:9000")
    metrics_link = page.get_by_role("link", name="Student Metrics")

    expect(metrics_link).to_have_test('Student Metrics')

    metrics_link.click()
    metric_data_heading = page.get_by_role("heading", name="Student Metrics").get_by_text("Student Metrics")

    expect(metric_data_heading).to_have_text("Student Metrics")
    return

def test_student_selectbox(page: Page):
    '''
    '''
    page.goto("http://localhost:9000/Student Metrics")
    select_student_sb = page.get_by_role("selectbox", name="Select Student")

    expect(select_student_sb).to_have_text('Leyla Hair')