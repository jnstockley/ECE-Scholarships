'''
Main Flet app interface for the streamlit server launcher application
'''
import pathlib
from multiprocessing import Process
import flet as ft
from streamlit.web import bootstrap

HERE = pathlib.Path(__file__).parent

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

        self.streamlit_process: Process | None  = None
        self.streamlit_running: bool = False

    def __handle_click(self, _e):
        '''
        Handles button click
        '''
        if not self.streamlit_running:
            self.streamlit_process = Process(target=start_streamlit, args=(HERE,))
            self.streamlit_process.start()
            self.streamlit_running = True
            return

        self.streamlit_process.kill()
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
