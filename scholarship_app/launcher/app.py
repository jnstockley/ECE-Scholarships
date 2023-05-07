'''
Main Flet app interface for the streamlit server launcher application
'''
import pathlib
import subprocess
import flet as ft
import os
import signal
from streamlit.web import bootstrap

HERE = pathlib.Path(__file__).parent
STREAMLIT_CMD = f"streamlit run {HERE.joinpath('../router.py')} --server.port 8501"

class StreamlitButton(ft.TextButton):
    '''
    Streamlit button toggle object

    Attributes
    ----------
    streamlit_running : bool
        True if streamlit process running
    streamlit_process : Process | None
        The active streamlit server process
    '''
    def __init__(self):
        super().__init__(text="Start Streamlit Server", on_click=self.__handle_click)

        self.streamlit_process = None
        self.streamlit_running: bool = False

    def __handle_click(self, _e):
        '''
        Handles button click
        '''
        if not self.streamlit_running:
            self.streamlit_process = subprocess.Popen(STREAMLIT_CMD, shell=True)
            self.streamlit_running = True
            return

        self.streamlit_process.send_signal(signal.SIGTERM)
        self.streamlit_running = False


def start_streamlit(here: str):
    '''
    Starts the streamlit server

    Parameters
    ----------
    root : str
        path of file in file system.
    '''
    bootstrap.run(
            str(here.joinpath("../router.py")),
            command_line=None,
            args=[],
            flag_options={},
        )

def home(page: ft.Page):
    '''
    Homepage of flet application
    '''
    page.add(StreamlitButton())
