from flet import Ref
from fletx import Xstate
from fletx.controls import Switch
import flet as ft
import random
import requests
from sqlmodel import create_engine, Field, SQLModel, Session, select


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

# 新增 News 模型
class News(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    time: str
    likes: int

# 创建数据库引擎（你可以根据实际情况调整数据库路径）
engine = create_engine("sqlite:///news.db")
SQLModel.metadata.create_all(engine)

class CommutePageState:
    
    def __init__(self):
        # 检查User表是否为空，若为空则插入随机用户
        with Session(engine) as session:
            if not session.exec(select(User)).first():
                names = [
                    "张三", "李四", "王五", "赵六", "小明", "小红", "Alice", "Bob"
                ]
                for name in random.sample(names, 5):
                    session.add(User(name=name))
                session.commit()
        self.page = self.build()

    def generate_random_text(self):
        response = requests.get("https://www.baidu.com")
        code_text = str(response.status_code)
        # 生成一些随机的文本数据
        titles = ["今天的新闻", "热点话题", "每日推荐", "科技资讯", "生活小贴士"]
        titles = [title + code_text for title in titles]
        contents = [
            "人工智能发展迅速，改变生活方式",
            "环保理念深入人心，绿色生活成为主流",
            "新能源汽车市场持续增长",
            "太空探索取得重大突破",
            "健康生活方式越来越受关注"
        ]
        
        data = []
        with Session(engine) as session:
            for _ in range(10):
                item = {
                    "title": random.choice(titles),
                    "content": random.choice(contents),
                    "time": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                    "likes": random.randint(100, 1000)
                }
                data.append(item)
                # 插入到数据库
                news = News(**item)
                session.add(news)
            session.commit()
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
        
        # 1. 查询所有用户
        with Session(engine) as session:
            users = session.query(User).all()

        # 2. 用 Flet 组件展示用户
        if users:
            user_list_column = ft.Column(
                controls=[
                    ft.Text("用户列表", size=18, weight=ft.FontWeight.BOLD),
                    *[
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON),
                            title=ft.Text(user.name)
                        ) for user in users
                    ]
                ],
                spacing=5
            )
            # 可以把用户列表加到滚动容器最前面
            scroll_container.content.controls.append(user_list_column)

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


