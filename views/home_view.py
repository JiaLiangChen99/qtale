from typing import cast

import flet as ft 
from fletx import Xview
from fletx.controls import Switch

from states.home_child_state import HomeState, ManagerState, FindState
from states.main_state import MainState
class HomeView(Xview):

    def build(self):        
        return ft.View(
            # 设置程序的头部信息
            appbar=ft.AppBar(
                title=ft.Text("Music"),
                center_title=True,
                bgcolor=ft.Colors.BLACK12,
                shape=ft.NotchShape.CIRCULAR,
            ),
            # 设置底部导航栏
            navigation_bar = ft.CupertinoNavigationBar(
                bgcolor=ft.Colors.BLACK12,
                inactive_color=ft.Colors.GREY,
                active_color=ft.Colors.WHITE,
                on_change=cast(MainState,self.state).change_nav,
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="听歌"),
                    ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="管歌"),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.BOOKMARK_BORDER,
                        selected_icon=ft.Icons.BOOKMARK,
                        label="查歌",
                    ),
                ]
            ),
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    expand=True,
                    padding=10,  # 添加一些内边距
                    content=Switch(
                        ref=self.state.nav_switch,
                        controls={
                            "0": cast(HomeState,self.state.home_view_state.home_state).build_home_page(),
                            "1": cast(ManagerState, self.state.home_view_state.manager_state).build_manager_page(),
                            "2": ft.Container(
                                expand=True,
                                content=ft.Text("Explore",size=30)
                            ),
                        }
                    )
                )
            ]
        )
    
