'''
Main application entry point.
'''
import pathlib
import flet as ft
from scholarship_app.launcher.app import home

HERE = pathlib.Path(__file__).parent

def app():
    '''
    Main application executable entry point.
    '''
    ft.app(target=home)

if __name__ == "__main__":
    app()
