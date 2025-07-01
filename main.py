import sys
sys.path.append('../../')

import flet as ft 
from fletx import Xapp,route
from states.main_state import MainState
from views.home_view import HomeView
from views.next_view import NextView


def main(page:ft.Page):
    page.title = "Flet & FletX Bottom Navigation"

    Xapp(
        page=page,
        state=MainState,
        routes=[
            route(route="/",view=HomeView),
            route(route="/next",view=NextView)
        ]
    )
    
ft.app(target=main)


