"""
Main Flet app interface for the streamlit server launcher application
"""
import pathlib
import subprocess
import signal
import flet as ft
from scholarship_app.managers.config import ConfigManager

HERE = pathlib.Path(__file__).parent
STREAMLIT_CMD = f"streamlit run {HERE.joinpath('../router.py')} --server.port 8501"
SHAREPOINT_CONFIG_KEY = "sharepoint_url"


class MainContainer(ft.Container):
    """
    Main flet container
    """

    def __init__(self):
        self.config = ConfigManager()
        self.toggle_button = ft.ElevatedButton(
            "Start Streamlit Server", on_click=self.__handle_toggle
        )

        current_sharepoint_value = ""
        if self.config.has_key(SHAREPOINT_CONFIG_KEY):
            current_sharepoint_value = self.config.data[SHAREPOINT_CONFIG_KEY]

        self.status_text = ft.Text("Server not active", text_align=ft.TextAlign.CENTER)
        self.sharepoint_link = ft.TextField(label="Sharepoint Link", value=current_sharepoint_value)
        self.update_sharepoint_btn = ft.OutlinedButton(
            "Update", on_click=self.__handle_update_sharepoint
        )

        main_col = ft.Column(
            [
                ft.Text(
                    "Status:",
                    text_align=ft.TextAlign.CENTER,
                    style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                ),
                self.status_text,
                self.toggle_button,
                ft.Text(
                    "Sharepoint Link:",
                    text_align=ft.TextAlign.CENTER,
                    style=ft.TextThemeStyle.HEADLINE_SMALL,
                ),
                ft.Row([self.sharepoint_link, self.update_sharepoint_btn]),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        super().__init__(
            content=main_col, alignment=ft.alignment.center, margin=ft.margin.all(10)
        )

        self.streamlit_process = None
        self.streamlit_running = False

    def get_sharepoint_link(self):
        """
        Interfaces with config manager to get the sharepoint link
        """
        if self.config.has_key(SHAREPOINT_CONFIG_KEY):
            return self.data[SHAREPOINT_CONFIG_KEY]
        return ""

    def start_streamlit(self):
        """
        Starts the streamlit server
        """
        if self.streamlit_running:
            return

        with subprocess.Popen(STREAMLIT_CMD, shell=True) as streamlit_process:
            self.streamlit_process = streamlit_process
            self.streamlit_running = True

    def stop_streamlit(self):
        """
        Stops the streamlit server
        """
        if not self.streamlit_running:
            return

        self.streamlit_process.send_signal(signal.SIGTERM)
        self.streamlit_running = False
        print("stopping streamlit")

    def toggle_streamlit(self):
        """
        Toggle streamlit server
        """
        if not self.streamlit_running:
            self.start_streamlit()
            return

        self.stop_streamlit()

    def update_status_text(self):
        """
        Updates the text below Status:
        """
        if self.streamlit_running:
            self.status_text.value = "Server running on port 8501"
        else:
            self.status_text.value = "Server not active"

        self.status_text.update()

    def update_toggle_text(self):
        """
        Update the toggle button text
        """
        if self.streamlit_running:
            self.toggle_button.text = "Stop streamlit server"
        else:
            self.toggle_button.text = "Start streamlit server"

        self.toggle_button.update()

    def __handle_update_sharepoint(self, _e):
        """
        Handles the update sharepoint onclick
        """
        self.config.set_value(SHAREPOINT_CONFIG_KEY, self.sharepoint_link.value)

    def __handle_toggle(self, _e):
        """
        Handles toggling of the server
        """
        self.toggle_streamlit()
        self.update_status_text()
        self.update_toggle_text()


# Register the signal handler
class FletApp:
    """
    Main fletapp launcher
    """

    def __init__(self):
        self.main_container: MainContainer = MainContainer()

    def run(self):
        """
        Runs the flet application
        """
        ft.app(target=self.home_page)

    def home_page(self, page):
        """
        Main homepage render
        """
        page.add(self.main_container)

    def kill_hanging_processes(self):
        """
        If users closes window, we want to kill the streamlit process running in background
        """
        self.main_container.stop_streamlit()
