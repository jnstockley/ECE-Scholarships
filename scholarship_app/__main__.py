'''
Main application entry point.
'''
import pathlib
import flet as ft

from streamlit.web import bootstrap
from scholarship_app.launcher.app import home

HERE = pathlib.Path(__file__).parent

def app():
    '''
    Main application executable entry point.
    '''
    ft.app(target=home)

    bootstrap.run(
        str(HERE.joinpath("router.py")),
        command_line=None,
        args=[],
        flag_options={},
    )


if __name__ == "__main__":
    app()
