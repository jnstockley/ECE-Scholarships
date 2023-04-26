'''
Main Flet app interface for the streamlit server launcher application
'''
import flet as ft

def home(page: ft.Page):
    '''
    Homepage of flet application
    '''
    def add_clicked(_e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        page.update()

    new_task = ft.TextField(hint_text="Whats needs to be done?")

    page.add(new_task, ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked))
