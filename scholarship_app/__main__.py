# Copyright 2022 Radiotherapy AI Pty Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib
import flet as ft

import streamlit.web.bootstrap as bootstrap

HERE = pathlib.Path(__file__).parent

def flet_app(page: ft.Page):
    def add_clicked(_e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        page.update()

    new_task = ft.TextField(hint_text="Whats needs to be done?")

    page.add(new_task, ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked))

def app():
    ft.app(target=flet_app)

    bootstrap.run(
        str(HERE.joinpath("app.py")),
        command_line=None,
        args=list(),
        flag_options=dict(),
    )


if __name__ == "__main__":
    app()
