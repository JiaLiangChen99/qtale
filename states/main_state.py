from flet import Ref
from fletx import Xstate
from fletx.controls import Switch
import flet as ft

class CommutePageState:
    
    def __init__(self):
        self.page = self.build()

    def load_first_page_data(self, render_new: bool=False):
        # 第一次渲染
        if render_new is True:
            pass
        else:
            for i in range(3):
                self.page.controls.append(ft.Text(f"CommutePageState{i}",size=30))

    def build(self):
        return ft.Column(
            expand=True,
            controls=[
                ft.Text("CommutePageState",size=30),
            ]
        )


class MainState(Xstate):

    def __init__(self, page):
        super().__init__(page)
        self.commute_page_states = CommutePageState()
        self.nav_switch = Ref[Switch]()
        self.second_page: Ref[ft.Column] = self.commute_page_states.page
        self.commute_page_activate: bool = False

    def change_nav(self,e):
        self.nav_switch.current.active = str(e.control.selected_index)
        # 这里直接调用上面的status做一些操作即可。
        if str(e.control.selected_index) == '1':
            self.commute_page_states.load_first_page_data(self.commute_page_activate)
            self.commute_page_activate = True
        self.update()


