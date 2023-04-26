'''
Main application entry point.
'''
import pathlib
import flet as ft

import streamlit.web.bootstrap as bootstrap
import launcher.app.home

HERE = pathlib.Path(__file__).parent

def app():
    '''
    Main application executable entry point.
    '''
    ft.app(target=home)

    bootstrap.run(
        str(HERE.joinpath("app.py")),
        command_line=None,
        args=list(),
        flag_options=dict(),
    )


if __name__ == "__main__":
    app()
