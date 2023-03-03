'''
Main entry point for streamlit app.
'''
from st_pages import Page, show_pages

# Specify what pages should be shown in the sidebar, and what their titles
# and icons should be
show_pages(
    [
        Page("src/pages/home.py", "Home"),
        Page("src/pages/import.py", "Import Data"),
        Page("src/pages/scholarship_management.py", "Scholarship Management"),
        Page("src/pages/student_metrics.py", "Student Metrics")
    ]
)
