"""
Main entry point for streamlit app. Sets up the page routing for the application.
"""
import pathlib
from st_pages import Page, show_pages

HERE = pathlib.Path(__file__).parent

show_pages(
    [
        Page(HERE.joinpath("pages/home.py"), "Home"),
        Page(
            HERE.joinpath("pages/scholarship_management.py"), "Scholarship Management"
        ),
        Page(HERE.joinpath("pages/account.py"), "Account"),
        Page(HERE.joinpath("pages/download.py"), "Download File"),
        Page(HERE.joinpath("pages/import.py"), "Import Data"),
        Page(HERE.joinpath("pages/export.py"), "Export Data"),
    ]
)
