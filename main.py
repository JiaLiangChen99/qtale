import sys
sys.path.append('../../')

import flet as ft 
from fletx import Xapp,route

from states.main_state import MainState
from views.home_view import HomeView
from views.detial_view import DetailView
from static import init_path

def main(page:ft.Page):
    page.title = "FletX music"
    init_path()
    Xapp(
        page=page,
        state=MainState,
        routes=[
            route(route="/",view=HomeView),
            route(route="/music_detail",view=DetailView)
        ]
    )
    
ft.app(target=main)