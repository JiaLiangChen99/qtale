import flet as ft


# define a song class as our model

class Song(object):
    def __init__(self, song_name: str, artist_name: str,
                 audio_path: str, img_path: str) -> None:
        super(Song, self).__init__()

        self.song_name = song_name
        self.artist_name = artist_name
        self.audio_path = audio_path
        self.img_path = img_path
    
    @property
    def name(self):
        return self.song_name
    
    @property
    def artist(self):
        return self.artist_name
    
    @property
    def path(self):
        return self.audio_path
    
    @property
    def path_img(self):
        return self.img_path


class AudioDirectory(object):
    playlist: list = [
        Song(
            song_name="Song 1",
            artist_name="Artist 1",
            audio_path="song1.mp3",
            img_path="song1.jpg"
        ),
        Song(
            song_name="Song 2",
            artist_name="Artist 2",
            audio_path="song2.mp3",
            img_path="song2.jpg"
        ),
    ]


class Playlist(ft.View):
    def __init__(self, page: ft.Page):
        super(Playlist, self).__init__(
            route="/playlist",
            horizontal_alignment="center",
        )
      
        self.page = page
        self.playlist: list[Song] = AudioDirectory.playlist

        self.controls = [
            ft.Row([
                ft.Text("Playlist", size=21, weight="bold"),

            ], alignment="center"),
            ft.Divider(height=10, color="orange")
        ]

        self.generate_playlist_ui()
      
    
        # 定义一个函数添加歌曲songs
    def generate_playlist_ui(self):
      for song in self.playlist:
          self.controls.append(
              self.create_song_row(
                  song.name, 
                  song.artist_name, 
                  song)
          )

    def create_song_row(self, song_name, artist, song: Song):
        return ft.Container(
            content=ft.Row([
                ft.Text(f"Title:{song.name}"),
                ft.Text(artist)
            ],
            alignment="spaceBetween"
            ),
            data=song,
            padding=10,
            on_click=self.toggle_song
        )

    def toggle_song(self, event):
        self.page.session.set("song", event.control.data)
        self.page.go("/song")
        ...

class CurreentSong(ft.View):
    def __init__(self, page: ft.Page):
        super(CurreentSong, self).__init__(
            route="/song",
            padding=20,
            horizontal_alignment="center",
            vertical_alignment="center"
        )
        self.page = page

        self.song: Song = self.page.session.get("song")
        self.create_audio_track()
        # 接下来我们定义一些变量来显示当前歌曲的信息
        self.duration: int = 0
        self.start: int = 0
        self.end: int = 0

        self.is_playing: bool = False

        # 定义ui
        self.txt_start = ft.Text(self.format_time(self.start))
        self.txt_end = ft.Text(self.format_time(self.end))

        self.slider = ft.Slider(min=0, thumb_color="transparent", 
                                on_change_end=None,
                                on_change=lambda e: self.toggle_seek(
                                    round(float(e.data))
                                ))

        self.back_btn = ft.TextButton(
            content=ft.Text("Playlist", color="black" if self.page.theme_mode == ft.ThemeMode.LIGHT else "while")
            , on_click=self.toggle_playlist
        )

        self.play_btn = self.create_toggle_button(ft.icons.PLAY_ARROW_ROUNDED, 2, self.play)

        self.controls = [
            ft.Row(
                [self.back_btn], alignment="start", 
            ),
            ft.Container(
                # height=1, 
                expand=True,
                border_radius=1,
                shadow=ft.BoxShadow(
                    # spread_radius=0.1,
                    # blur_radius=0.1,
                    color=ft.colors.with_opacity(0.1, "black")
                ),
                image=ft.DecorationImage(src=self.song.path_img)
            ),
            ft.Divider(height=40, color="transparent"),
            ft.Column(
                [
                    ft.Row(
                        controls=[ft.Text(self.song.name, size=18, weight="bold")]
                    ),
                    ft.Row(
                        controls=[ft.Text(self.song.artist_name, size=14, opacity=0.81)]
                    )
                ],
                spacing=1,
            ),
            ft.Divider(height=10, color="transparent"),
            ft.Column(
                [
                    ft.Row([self.txt_start, self.txt_end],
                           alignment="spaceBetween"),
                    self.slider
                ],
                spacing=0
            ),
            ft.Divider(height=10, color="transparent"),
            ft.Row(
                [
                    self.create_toggle_button(ft.icons.REPLAY_10_SHARP, 
                                              0.9,
                                     lambda e: self.__update_position(-5000)),
                    self.play_btn,
                    self.create_toggle_button(ft.icons.FORWARD_10_SHARP, 
                                              0.9,
                                     lambda e: self.__update_position(5000)),
                ],
                alignment="spaceEvenly"
            )
        ]

    

    def play(self, e):
        self.toggle_play_pause()
        self.duration = self.audio.get_duration()
        self.end = self.duration
        self.slider.max = self.duration
        ...

    # 更新play/pause
    def toggle_play_pause(self, event=None):
        if self.is_playing:
            self.play_btn.icon = ft.icons.PLAY_ARROW_ROUNDED
            self.audio.pause()
        else:
            self.play_btn.icon = ft.icons.PAUSE_ROUNDED
            try:
                self.audio.resume()
            except:
                self.audio.play()
        self.is_playing = False if self.is_playing else True

        #self.play_btn.on_click = self.toggle_play_pause()
        self.play_btn.update()

    def __update_start_end(self):
        if self.start < 0:
            self.start = 0
        if self.end > self.duration:
            self.end = self.duration

    def __update_position(self, delta: int):
        self.__update_start_end()
        if self.start > 0:
            if delta == 5000:
                post_change = 5000
            elif delta == -5000:
                post_change = -5000
            
            pos = self.start + post_change
            self.audio.seek(pos)

            self.start += post_change
            self.end -= post_change
        pass

    def __update_slider(self, delta: int):
        self.slider.value = delta
        self.slider.update()

    def __update_time_stamps(self, start, end):
        self.txt_start.value = self.format_time(self.start)
        self.txt_end.value = f"-{self.format_time(self.end)}"
        self.txt_start.update() 
        self.txt_end.update()

    def toggle_seek(self, delta):
        self.start = delta
        self.end = self.duration - delta
        self.audio.seek(self.start)
        self.__update_slider(delta)

    def __update(self, delta: int):
        self.start += 1000
        self.end -= 1000
        # 更新slider
        self.__update_slider(delta)
        # 更新时间
        self.__update_time_stamps(self.start, self.end)
        # 格式化时间
      
    def format_time(self, value: int):
        milliseconds = value
        minutes, second = divmod(milliseconds / 1000, 60)
        formatted_time = "{:02}:{:02}".format(int(minutes), int(second))
        return formatted_time

    def create_audio_track(self):
        self.audio = ft.Audio(src=self.song.path,
                     on_position_changed=lambda e: self.__update(
                         int(e.data)
                     ))
        self.page.overlay.append(self.audio)

    def create_toggle_button(self, icon, scale, function):
        return ft.IconButton(icon=icon, scale=scale, on_click=function)

    def toggle_playlist(self, e):
        # 当我们要返回到歌曲单
        self.audio.pause()
        self.page.session.clear()
        self.page.go("/playlist")

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    
    def router(route):
        page.views.clear()
        if page.route == "/playlist":
            playlist = Playlist(page)
            page.views.append(playlist)
        elif page.route == "/song":
            song = CurreentSong(page)
            page.views.append(song)
        

        page.update()
        ...

    page.on_route_change = router
    page.go("/playlist")
  
if __name__ == "__main__":
    ft.app(target=main)