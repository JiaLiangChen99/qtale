import sys
sys.path.append('../../')

import flet as ft 
from fletx import Xapp,route

from states.main_state import MainState
from views.home_view import HomeView
from views.detial_view import DetailView
from static import init_path, print_storage_info

def main(page:ft.Page):
    page.title = "FletX music"
    
    # 初始化存储路径
    init_path()
    
    # 打印存储信息（用于调试）
    print_storage_info()
    
    # 注意：数据库初始化现在在global_state中自动处理
    print("应用初始化完成")
    
    Xapp(
        page=page,
        state=MainState,
        routes=[
            route(route="/",view=HomeView),
            route(route="/music_detail",view=DetailView)
        ]
    )

if __name__ == "__main__":
    ft.app(target=main)