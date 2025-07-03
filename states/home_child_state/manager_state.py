from fletx import Xstate
import flet as ft
import os
import shutil

from static import MUSIC_PATH, IMAGE_PATH
from states.global_state import home_view_global_state
from states.model import SessionLocal, Music

class ManagerState(Xstate):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.add_title_field = ft.TextField(label="标题")
        self.add_description_field = ft.TextField(label="描述")
        self.add_music_file_picker = ft.FilePicker(
            on_result=self.pick_files_result
        )
        self.page.overlay.append(self.add_music_file_picker)
        # 创建音乐列表容器，使用动态列表
        self.music_list_column = ft.Column(
            controls=[],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        # 创建基础组件
        self.base_component = ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("音乐管理", size=24, weight=ft.FontWeight.BOLD),
                    # 使用动态音乐列表
                    ft.Container(
                        content=self.music_list_column,
                        expand=True,
                        padding=ft.padding.all(10)
                    ),
                    ft.Container(height=30),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        text="创建音乐",
                        on_click=lambda e: self.page.open(self.dlg_modal)
                    )
                ]
            )
        )
        # 标记是否已经加载过音乐列表
        self.music_list_loaded = False
        # 修改对话框为添加音乐表单
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("添加音乐"),
            content=ft.Column(
                width=400,
                height=200,
                controls=[
                    self.add_title_field,
                    self.add_description_field,
                    ft.ElevatedButton(
                        "选择音乐文件",
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=lambda _: self.add_music_file_picker.pick_files(
                            allow_multiple=False,
                            allowed_extensions=["mp3", "wav", "flac", "m4a", "ogg"]
                        ),
                    )
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("取消", on_click=self.close_dialog),
                ft.ElevatedButton("确定", on_click=self.save_music),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("添加音乐对话框已关闭!"),
        )
        # 存储选择的文件路径
        self.selected_file_path = None
        
    def load_music_list(self):
        """加载音乐列表到动态列表中"""
        self.music_list_column.controls.clear()
        
        # 检查数据库状态
        if not home_view_global_state.is_ready():
            # 显示数据库未就绪的提示
            error_card = ft.Card(
                content=ft.Container(
                    padding=ft.padding.all(20),
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.ERROR, size=40, color=ft.Colors.RED),
                            ft.Text(
                                "数据库未就绪",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.RED
                            ),
                            ft.Text(
                                "请检查应用存储权限或重启应用",
                                size=14,
                                color=ft.Colors.GREY_600
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
            self.music_list_column.controls.append(error_card)
        elif len(home_view_global_state.global_music) == 0:
            # 显示空列表提示
            empty_card = ft.Card(
                content=ft.Container(
                    padding=ft.padding.all(20),
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.MUSIC_NOTE, size=40, color=ft.Colors.GREY),
                            ft.Text(
                                "暂无音乐",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_600
                            ),
                            ft.Text(
                                "点击下方按钮添加你的第一首音乐",
                                size=14,
                                color=ft.Colors.GREY_500
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
            self.music_list_column.controls.append(empty_card)
        else:
            # 显示音乐列表
            for music in home_view_global_state.global_music:
                music_card = ft.Card(
                    content=ft.Container(
                        padding=ft.padding.all(15),
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.MUSIC_NOTE, size=30, color=ft.Colors.BLUE),
                                        ft.Container(width=10),
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    music.title,
                                                    size=16,
                                                    weight=ft.FontWeight.BOLD
                                                ),
                                                ft.Text(
                                                    music.description or "无描述",
                                                    size=12,
                                                    color=ft.Colors.GREY_600
                                                ),
                                                ft.Text(
                                                    f"文件: {os.path.basename(music.music_path)}",
                                                    size=10,
                                                    color=ft.Colors.GREY_500
                                                )
                                            ],
                                            spacing=2,
                                            expand=True
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED,
                                            tooltip="删除音乐",
                                            on_click=lambda e, m=music: self.delete_music(m)
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.START
                                )
                            ]
                        )
                    ),
                    elevation=2,
                    margin=ft.margin.only(bottom=10)
                )
                self.music_list_column.controls.append(music_card)
        
        # 只有在控件已经添加到页面中时才更新
        try:
            if hasattr(self.music_list_column, 'page') and self.music_list_column.page:
                self.music_list_column.update()
        except:
            pass  # 如果更新失败，忽略错误
        
    def delete_music(self, music: Music):
        """删除音乐"""
        # 检查数据库是否就绪
        if not home_view_global_state.is_ready():
            print("数据库未就绪，无法删除音乐")
            return
            
        try:
            # 从数据库删除
            with SessionLocal() as session:
                session.delete(session.merge(music))
                session.commit()
            
            # 删除文件
            if os.path.exists(music.music_path):
                os.remove(music.music_path)
            
            # 刷新全局状态
            home_view_global_state.reload_music()
            
            # 只重新加载音乐列表
            self.load_music_list()
            
            print(f"成功删除音乐: {music.title}")
            
        except Exception as ex:
            print(f"删除音乐失败: {str(ex)}")
        
    def close_dialog(self, e):
        """关闭对话框并清空表单"""
        self.add_title_field.value = ""
        self.add_description_field.value = ""
        self.selected_file_path = None
        self.page.close(self.dlg_modal)
        
    def save_music(self, e):
        """保存音乐到数据库"""
        # 检查数据库是否就绪
        if not home_view_global_state.is_ready():
            print("数据库未就绪，无法保存音乐")
            # 可以在这里显示用户友好的错误消息
            return
            
        try:
            # 创建新的Music对象
            new_music = Music(
                title=self.add_title_field.value,
                description=self.add_description_field.value,
                music_path=self.selected_file_path
            )
            
            # 保存到数据库
            with SessionLocal() as session:
                session.add(new_music)
                session.commit()
                
            # 刷新全局音乐列表
            home_view_global_state.reload_music()
            
            # 关闭对话框
            self.close_dialog(e)
            
            # 只重新加载音乐列表，不重绘整个页面
            self.load_music_list()
            
            print(f"成功保存音乐: {new_music.title}")
            
        except Exception as ex:
            print(f"保存失败: {str(ex)}")
        
    def pick_files_result(self, e: ft.FilePickerResultEvent):
        """处理文件选择结果"""
        if e.files:
            file = e.files[0]
            file_name = file.name
            source_path = file.path
            self.add_description_field.value = source_path
            self.add_title_field.value = file_name
            self.update()
            try:
                # 确保MUSIC_PATH目录存在
                if not os.path.exists(MUSIC_PATH):
                    os.makedirs(MUSIC_PATH)
                
                # 生成目标文件路径
                destination_path = os.path.join(MUSIC_PATH, file_name)
                
                # 如果文件已存在，添加数字后缀
                counter = 1
                name_part, ext_part = os.path.splitext(file_name)
                while os.path.exists(destination_path):
                    new_name = f"{name_part}_{counter}{ext_part}"
                    destination_path = os.path.join(MUSIC_PATH, new_name)
                    counter += 1
                
                # 复制文件到目标目录
                shutil.copy2(source_path, destination_path)
                
                # 保存文件路径
                self.selected_file_path = destination_path
                
            except Exception as ex:
                self.selected_file_path = None

    def build_manager_page(self) -> ft.Container:
        # 首次加载时初始化音乐列表
        if not self.music_list_loaded:
            self.load_music_list()
            self.music_list_loaded = True
        
        return self.base_component