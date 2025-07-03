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
        
    def close_dialog(self, e):
        """关闭对话框并清空表单"""
        self.add_title_field.value = ""
        self.add_description_field.value = ""
        self.selected_file_path = None
        self.page.close(self.dlg_modal)
        
    def save_music(self, e):
        """保存音乐到数据库"""
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
            
            # 显示成功消息
            # self.page.show_snack_bar(ft.SnackBar(content=ft.Text("音乐添加成功!")))
            
            # 关闭对话框
            self.close_dialog(e)
            # 更新页面
            self.update()
            
        except Exception as ex:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"保存失败: {str(ex)}")))
        
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

    def reload_music_list(self):
        home_view_global_state.reload_music()
        self.page.update()

    def build_manager_page(self) -> ft.Container:
        # 将dialog添加到页面
        
        return ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("音乐管理", size=24, weight=ft.FontWeight.BOLD),
                    *[
                        ft.Card(
                            content=ft.ListTile(
                                title=ft.Text(music.title),
                                subtitle=ft.Text(music.description or ""),
                                trailing=ft.Text(music.music_path.split("/")[-1]),
                                # 你可以实现edit_music方法用于编辑
                                # on_click=lambda e, m=music: self.edit_music(m)
                            )
                        )
                        for music in home_view_global_state.global_music
                    ],
                    ft.Container(height=30),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        text="创建音乐",
                        on_click=lambda e: self.page.open(self.dlg_modal)
                    )
                ]
            )
        )