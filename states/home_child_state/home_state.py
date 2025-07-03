from typing import Callable
from dataclasses import dataclass
import random
import base64
import os
from enum import Enum

import flet as ft
from fletx import Xstate

from static import MUSIC_PATH, IMAGE_PATH
from ..global_state import home_view_global_state
from ..model import Music

class PlayMode(Enum):
    """播放模式枚举"""
    LOOP_ALL = "循环播放"
    LOOP_SINGLE = "单曲循环"
    RANDOM = "随机播放"
    SEQUENTIAL = "顺序播放"

class HomeState(Xstate):
    def __init__(self, page):
        super().__init__(page)

        self.music_list: list[Music] = home_view_global_state.global_music
        self.music_list_container: list[ft.Container] = []
        
        # 播放模式
        self.play_mode = PlayMode.LOOP_ALL
        
        # 创建音频播放器 - 设置一个默认的空src以避免错误
        self.audio_player = ft.Audio(
            src="https://github.com/mdn/webaudio-examples/blob/main/audio-basics/outfoxing.mp3?raw=true",  # 设置默认空src
            autoplay=False,
            volume=1.0,
            on_state_changed=self.on_audio_state_changed,
            on_position_changed=self.on_position_changed,
            on_duration_changed=self.on_duration_changed
        )
        self.page.overlay.append(self.audio_player)
        
        # 当前播放状态
        self.current_playing_music = None
        self.is_playing = False
        self.current_position = 0
        self.total_duration = 0
        
        # 控制条组件
        self.play_pause_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_size=40,
            on_click=self.toggle_play_pause
        )
        
        # 播放模式按钮
        self.play_mode_button = ft.IconButton(
            icon=ft.Icons.REPEAT,
            icon_size=25,
            tooltip=self.play_mode.value,
            on_click=self.toggle_play_mode
        )
        
        self.current_music_title = ft.Text("未选择音乐", size=16, weight=ft.FontWeight.BOLD)
        self.position_text = ft.Text("00:00", size=12)
        self.duration_text = ft.Text("00:00", size=12)
        
        self.progress_bar = ft.ProgressBar(
            value=0,
            width=300,
            height=4,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.BLUE
        )
        
        # 创建音乐控制条
        self.music_control_bar = ft.Container(
            height=80,
            bgcolor=ft.Colors.GREY_100,
            padding=ft.padding.all(10),
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=60,
                        height=60,
                        bgcolor=ft.Colors.BLUE_100,
                        border_radius=8,
                        content=ft.Icon(ft.Icons.MUSIC_NOTE, size=30, color=ft.Colors.BLUE)
                    ),
                    ft.Container(width=10),
                    ft.Column(
                        controls=[
                            self.current_music_title,
                            ft.Row(
                                controls=[
                                    self.position_text,
                                    ft.Container(
                                        content=self.progress_bar,
                                        margin=ft.margin.symmetric(horizontal=10)
                                    ),
                                    self.duration_text
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        spacing=5,
                        expand=True
                    ),
                    ft.Row(
                        controls=[
                            self.play_mode_button,
                            ft.IconButton(
                                icon=ft.Icons.SKIP_PREVIOUS,
                                icon_size=30,
                                on_click=self.previous_music
                            ),
                            self.play_pause_button,
                            ft.IconButton(
                                icon=ft.Icons.SKIP_NEXT,
                                icon_size=30,
                                on_click=self.next_music
                            )
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    def toggle_play_mode(self, e):
        """切换播放模式"""
        modes = list(PlayMode)
        current_index = modes.index(self.play_mode)
        next_index = (current_index + 1) % len(modes)
        self.play_mode = modes[next_index]
        
        # 更新播放模式按钮图标和提示
        mode_icons = {
            PlayMode.LOOP_ALL: ft.Icons.REPEAT,
            PlayMode.LOOP_SINGLE: ft.Icons.REPEAT_ONE,
            PlayMode.RANDOM: ft.Icons.SHUFFLE,
            PlayMode.SEQUENTIAL: ft.Icons.PLAY_ARROW
        }
        
        self.play_mode_button.icon = mode_icons[self.play_mode]
        self.play_mode_button.tooltip = self.play_mode.value
        
        print(f"播放模式切换为: {self.play_mode.value}")
        self.update_control_bar()

    def get_next_music_index(self):
        """根据播放模式获取下一首音乐的索引"""
        if not self.music_list:
            return -1
        
        # 刷新音乐列表
        self.music_list = home_view_global_state.global_music
        
        if not self.music_list:
            return -1
        
        current_index = -1
        if self.current_playing_music:
            for i, music in enumerate(self.music_list):
                if music.id == self.current_playing_music.id:
                    current_index = i
                    break
        
        if self.play_mode == PlayMode.LOOP_SINGLE:
            # 单曲循环：返回当前索引
            return current_index if current_index >= 0 else 0
        elif self.play_mode == PlayMode.RANDOM:
            # 随机播放：随机选择一首（避免选择当前播放的）
            available_indices = [i for i in range(len(self.music_list)) if i != current_index]
            if available_indices:
                return random.choice(available_indices)
            else:
                return 0
        else:
            # 循环播放和顺序播放
            if current_index >= len(self.music_list) - 1:
                if self.play_mode == PlayMode.LOOP_ALL:
                    return 0  # 循环到第一首
                else:  # SEQUENTIAL
                    return -1  # 顺序播放结束
            else:
                return current_index + 1

    def get_previous_music_index(self):
        """根据播放模式获取上一首音乐的索引"""
        if not self.music_list:
            return -1
        
        # 刷新音乐列表
        self.music_list = home_view_global_state.global_music
        
        if not self.music_list:
            return -1
        
        current_index = -1
        if self.current_playing_music:
            for i, music in enumerate(self.music_list):
                if music.id == self.current_playing_music.id:
                    current_index = i
                    break
        
        if self.play_mode == PlayMode.LOOP_SINGLE:
            # 单曲循环：返回当前索引
            return current_index if current_index >= 0 else 0
        elif self.play_mode == PlayMode.RANDOM:
            # 随机播放：随机选择一首（避免选择当前播放的）
            available_indices = [i for i in range(len(self.music_list)) if i != current_index]
            if available_indices:
                return random.choice(available_indices)
            else:
                return 0
        else:
            # 循环播放和顺序播放
            if current_index <= 0:
                if self.play_mode == PlayMode.LOOP_ALL:
                    return len(self.music_list) - 1  # 循环到最后一首
                else:  # SEQUENTIAL
                    return -1  # 顺序播放开始
            else:
                return current_index - 1

    def auto_play_next(self):
        """自动播放下一首音乐"""
        print(f"音乐播放完毕，当前播放模式: {self.play_mode.value}")
        
        next_index = self.get_next_music_index()
        
        if next_index >= 0 and next_index < len(self.music_list):
            next_music = self.music_list[next_index]
            print(f"自动播放下一首: {next_music.title}")
            self.play_music(next_music)
        elif self.play_mode == PlayMode.SEQUENTIAL:
            print("顺序播放已结束")
            self.is_playing = False
            self.current_playing_music = None
            self.update_control_bar()
            self.load_page()
        else:
            print("没有更多音乐可播放")

    def convert_audio_to_base64(self, file_path: str) -> str:
        """将音频文件转换为base64编码"""
        try:
            with open(file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                base64_string = base64.b64encode(audio_data).decode('utf-8')
                return base64_string
        except Exception as e:
            print(f"转换音频文件到base64失败: {e}")
            return None

    def format_time(self, milliseconds: int) -> str:
        """格式化时间显示"""
        if milliseconds <= 0:
            return "00:00"
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def play_music(self, music: Music):
        """播放指定音乐"""
        try:
            # 检查文件是否存在
            if not os.path.exists(music.music_path):
                print(f"音乐文件不存在: {music.music_path}")
                # 如果文件不存在，尝试播放下一首
                if self.play_mode != PlayMode.SEQUENTIAL:
                    self.auto_play_next()
                return
            
            # 如果正在播放音乐，先释放资源
            if self.current_playing_music:
                self.audio_player.release()
                print("释放之前的音频资源")
            
            # 转换为base64并播放
            base64_data = self.convert_audio_to_base64(music.music_path)
            if base64_data:
                # 设置新的音频源
                self.audio_player.src = ""
                self.audio_player.src_base64 = base64_data
                
                # 更新播放状态
                self.current_playing_music = music
                self.is_playing = True
                
                # 播放音乐
                self.audio_player.play()
                
                print(f"开始播放: {music.title}")
                
                # 更新控制条显示
                self.update_control_bar()
                
                # 重新加载音乐列表以更新显示状态
                self.load_page()
                
            else:
                print("无法加载音乐文件")
                # 如果转换失败，尝试播放下一首
                if self.play_mode != PlayMode.SEQUENTIAL:
                    self.auto_play_next()
                
        except Exception as e:
            print(f"播放音乐失败: {e}")
            # 如果播放失败，尝试播放下一首
            if self.play_mode != PlayMode.SEQUENTIAL:
                self.auto_play_next()

    def toggle_play_pause(self, e):
        """切换播放/暂停"""
        if self.current_playing_music:
            if self.is_playing:
                self.audio_player.pause()
                self.is_playing = False
                print("暂停播放")
            else:
                self.audio_player.resume()
                self.is_playing = True
                print("恢复播放")
            self.update_control_bar()
        else:
            print("没有选择音乐")

    def previous_music(self, e):
        """上一首音乐"""
        previous_index = self.get_previous_music_index()
        
        if previous_index >= 0 and previous_index < len(self.music_list):
            previous_music = self.music_list[previous_index]
            print(f"切换到上一首: {previous_music.title}")
            self.play_music(previous_music)
        else:
            print("没有上一首音乐")

    def next_music(self, e):
        """下一首音乐"""
        next_index = self.get_next_music_index()
        
        if next_index >= 0 and next_index < len(self.music_list):
            next_music = self.music_list[next_index]
            print(f"切换到下一首: {next_music.title}")
            self.play_music(next_music)
        else:
            print("没有下一首音乐")

    def update_control_bar(self):
        """更新控制条显示"""
        if self.current_playing_music:
            self.current_music_title.value = self.current_playing_music.title
            self.play_pause_button.icon = ft.Icons.PAUSE if self.is_playing else ft.Icons.PLAY_ARROW
        else:
            self.current_music_title.value = "未选择音乐"
            self.play_pause_button.icon = ft.Icons.PLAY_ARROW
        
        self.position_text.value = self.format_time(self.current_position)
        self.duration_text.value = self.format_time(self.total_duration)
        
        if self.total_duration > 0:
            self.progress_bar.value = self.current_position / self.total_duration
        else:
            self.progress_bar.value = 0
            
        self.update()

    def on_audio_state_changed(self, e):
        """音频状态改变事件"""
        print(f"音频状态改变: {e.data}")
        if e.data == "completed":
            # 音乐播放完毕，根据播放模式自动处理
            self.auto_play_next()
        elif e.data == "paused":
            self.is_playing = False
            self.update_control_bar()
        elif e.data == "playing":
            self.is_playing = True
            self.update_control_bar()
        elif e.data == "stopped":
            self.is_playing = False
            self.update_control_bar()

    def on_position_changed(self, e):
        """音频位置改变事件"""
        if hasattr(e, 'data') and e.data:
            self.current_position = int(e.data)
            # 只在播放时更新控制条，避免频繁更新
            if self.is_playing:
                self.update_control_bar()

    def on_duration_changed(self, e):
        """音频时长改变事件"""
        if hasattr(e, 'data') and e.data:
            self.total_duration = int(e.data)
            print(f"音频时长: {self.format_time(self.total_duration)}")
            self.update_control_bar()

    def load_page(self):
        """加载音乐列表页面"""
        self.music_list = home_view_global_state.global_music
        self.music_list_container = []
        
        for music in self.music_list:
            # 判断是否是当前播放的音乐
            is_current_playing = (self.current_playing_music and 
                                self.current_playing_music.id == music.id)
            
            # 创建音乐卡片
            music_card = ft.Card(
                content=ft.Container(
                    padding=ft.padding.all(15),
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.Colors.BLUE_100 if is_current_playing else ft.Colors.GREY_200,
                                border_radius=8,
                                content=ft.Icon(
                                    ft.Icons.MUSIC_NOTE,
                                    size=25,
                                    color=ft.Colors.BLUE if is_current_playing else ft.Colors.GREY_600
                                )
                            ),
                            ft.Container(width=15),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        music.title,
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE if is_current_playing else ft.Colors.BLACK
                                    ),
                                    ft.Text(
                                        music.description or "无描述",
                                        size=14,
                                        color=ft.Colors.GREY_600
                                    ),
                                    ft.Text(
                                        f"文件: {os.path.basename(music.music_path)}",
                                        size=12,
                                        color=ft.Colors.GREY_500
                                    )
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.Icons.PLAY_ARROW if not is_current_playing else (ft.Icons.PAUSE if self.is_playing else ft.Icons.PLAY_ARROW),
                                icon_size=30,
                                icon_color=ft.Colors.BLUE,
                                on_click=lambda e, m=music: self.play_music(m) if not is_current_playing else self.toggle_play_pause(e)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ),
                elevation=2,
                margin=ft.margin.only(bottom=10)
            )
            
            self.music_list_container.append(music_card)
        
        self.update()

    def build_home_page(self) -> ft.Container:
        return self.page_build(lambda:self.go("/music_detail"))

    def page_build(self, function: Callable):
        self.load_page()
        return ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.padding.all(20),
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("我的歌曲", size=28, weight=ft.FontWeight.BOLD),
                                        ft.Container(expand=True),
                                        ft.Text(f"播放模式: {self.play_mode.value}", size=12, color=ft.Colors.GREY_600)
                                    ]
                                ),
                                ft.Container(height=10),
                                ft.ElevatedButton(
                                    "音乐管理",
                                    icon=ft.Icons.SETTINGS,
                                    on_click=lambda e: function()
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            controls=self.music_list_container,
                            scroll=ft.ScrollMode.AUTO
                        ),
                        padding=ft.padding.symmetric(horizontal=20)
                    ),
                    # 底部音乐控制条
                    self.music_control_bar
                ]
            )
        )