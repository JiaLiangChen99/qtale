from fletx import Xview
import flet as ft 

class NextView(Xview):
    # 没有appbar的信息？
    def build(self):
        return ft.View(
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Next View",size=30),
                ft.ElevatedButton("<< Back",on_click= self.back),
            ]
        )