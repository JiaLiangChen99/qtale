from dataclasses import dataclass
from .model import Music, engine, SessionLocal


class HomeViewGlobalState():
    def __init__(self):
        self.global_music: list[Music] = []
        self.reload_music()

    def reload_music(self):
        with SessionLocal() as session:
            self.global_music = session.query(Music).all()
        

home_view_global_state = HomeViewGlobalState()
