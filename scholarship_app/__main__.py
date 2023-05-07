'''
Main application entry point.
'''
import pathlib
from scholarship_app.launcher.app import FletApp

HERE = pathlib.Path(__file__).parent

if __name__ == "__main__":
    app = FletApp()
    app.run()
    app.kill_hanging_processes()
