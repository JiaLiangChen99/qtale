from typing import Callable
from dataclasses import dataclass
import random

import flet as ft
from fletx import Xstate

from static import MUSIC_PATH, IMAGE_PATH
from ..global_state import home_view_global_state
from ..model import Music

class HomeState(Xstate):
    def __init__(self, page):
        super().__init__(page)

        self.music_list: list[Music] = home_view_global_state.global_music
        self.music_list_container: list[ft.Container] = []

  

    def load_page(self):
        if len(self.music_list_container) > 0:
            return
        else:
            self.music_list_container = []
        for music in self.music_list:
            self.music_list_container.append(
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.Text(music.title, size=30)
                        ]
                    )
                )
            )
        self.update()


    def build_home_page(self) -> ft.Container:
        return self.page_build(lambda:self.go("/music_detail"))


    def page_build(
        self, function: Callable
    ):
        self.load_page()
        return ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.Text("我的歌曲预览",size=30),
                            ft.ElevatedButton("Go Next View",on_click=lambda  e:function())
                        ] + self.music_list_container
                    )
                )