from dataclasses import dataclass
from .model import Music, engine, SessionLocal, ensure_tables_exist


class HomeViewGlobalState():
    def __init__(self):
        self.global_music: list[Music] = []
        self.database_ready = False
        
        # 确保数据库表存在后再加载数据
        try:
            self.database_ready = ensure_tables_exist()
            if self.database_ready:
                self.reload_music()
            else:
                print("数据库初始化失败，将使用空的音乐列表")
        except Exception as e:
            print(f"数据库初始化过程中发生错误: {e}")
            self.database_ready = False

    def reload_music(self):
        """重新加载音乐数据"""
        if not self.database_ready:
            print("数据库未就绪，无法加载音乐数据")
            return
            
        try:
            with SessionLocal() as session:
                self.global_music = session.query(Music).all()
                print(f"成功加载 {len(self.global_music)} 首音乐")
        except Exception as e:
            print(f"加载音乐数据失败: {e}")
            self.global_music = []
            # 如果查询失败，可能是数据库问题，尝试重新初始化
            try:
                print("尝试重新初始化数据库...")
                self.database_ready = ensure_tables_exist()
            except Exception as e2:
                print(f"重新初始化数据库也失败: {e2}")

    def is_ready(self):
        """检查数据库是否就绪"""
        return self.database_ready


home_view_global_state = HomeViewGlobalState()
