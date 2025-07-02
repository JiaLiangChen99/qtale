from flet import Ref
from fletx import Xstate
from fletx.controls import Switch
import flet as ft
import random
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLAlchemy基础设置
Base = declarative_base()
engine = create_engine("sqlite:///news.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

# 创建表
Base.metadata.create_all(engine)

class CommutePageState:    
    def __init__(self):
        # 检查User表是否为空，若为空则插入随机用户
        session = SessionLocal()
        if not session.query(User).first():
            names = ["张三", "李四", "王五", "赵六", "小明", "小红", "Alice", "Bob"]
            for name in random.sample(names, 5):
                session.add(User(name=name))
            session.commit()
        session.close()
        self.page = self.build()

    def generate_random_text(self):
        titles = ["今天的新闻", "热点话题", "每日推荐", "科技资讯", "生活小贴士"]
        contents = [
            "人工智能发展迅速，改变生活方式",
            "环保理念深入人心，绿色生活成为主流",
            "新能源汽车市场持续增长",
            "太空探索取得重大突破",
            "健康生活方式越来越受关注"
        ]
        
        data = []
        for _ in range(10):
            item = {
                "title": random.choice(titles),
                "content": random.choice(contents),
                "time": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                "likes": random.randint(100, 1000)
            }
            data.append(item)
        return data

    def load_first_page_data(self, render_new: bool=False):
        if render_new is True:
            return
        
        # 创建一个固定高度的容器来放置滚动内容
        scroll_container = ft.Container(
            height=500,  # 设置固定高度
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                controls=[]
            ),
            border=ft.border.all(1, ft.Colors.BLACK12),  # 添加边框便于查看区域
            border_radius=10,
        )
        
        # 3. 资讯卡片
        random_data = self.generate_random_text()
        for item in random_data:
            scroll_container.content.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.ARTICLE),
                                title=ft.Text(
                                    item["title"],
                                    size=20,
                                    weight=ft.FontWeight.BOLD
                                ),
                                subtitle=ft.Text(
                                    f"发布时间: {item['time']}"
                                ),
                            ),
                            ft.Container(
                                content=ft.Text(
                                    item["content"],
                                    size=16
                                ),
                                padding=ft.padding.only(left=15, right=15, bottom=15)
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.THUMB_UP, size=16),
                                    ft.Text(f"{item['likes']}"),
                                ]),
                                padding=ft.padding.only(left=15, bottom=10)
                            )
                        ]),
                        padding=10
                    ),
                    margin=10
                )
            )
        
        # 将滚动容器添加到页面中
        self.page.controls.append(scroll_container)

    def build(self):
        return ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    content=ft.Text(
                        "每日资讯",
                        size=30,
                        weight=ft.FontWeight.BOLD
                    ),
                    padding=ft.padding.all(20)
                ),
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


