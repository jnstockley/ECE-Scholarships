'''
Main application entry point.
'''
import multiprocessing
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
    # See: https://pyoxidizer.readthedocs.io/en/stable/pyoxidizer_packaging_multiprocessing.html#spawn-only-works-on-windows-with-pyoxidizer
    #multiprocessing.set_start_method("auto", force=True)

    app()
