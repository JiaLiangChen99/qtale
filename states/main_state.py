from flet import Ref
from fletx import Xstate
from fletx.controls import Switch

from .home_view_state import HomeViewState

class MainState(Xstate):
    def __init__(self, page):
        super().__init__(page)
        self.nav_switch = Ref[Switch]()
        # Home mutipage state
        self.home_view_state = HomeViewState(page)
        self.app_global_count: int = 0

    def change_nav(self,e):
        self.nav_switch.current.active = str(e.control.selected_index)
        self.update()
