from flet import *
import flet as ft



class CreateTask(ft.View):
    def __init__(self, page: Page):
        super(CreateTask, self).__init__(
            route="/create_task",
            horizontal_alignment="center"
        )
        self.bgcolor = '#3450a1'
        self.page = page

        self.controls = [
            Text(value="X")
        ]


class Index(ft.View):
    FWG = "#97b4ff"
    FG = "#3450a1"
    PINK = "#eb06ff"
    

    def __init__(self, page: Page):
        super(Index, self).__init__(
            route="/",
            horizontal_alignment="center"
        )
        self.bgcolor = '#3450a1'
        self.page = page

        categories_card = Row(
            scroll='auto'
        )
        categories = ['Business', 'Family', 'Friends']
        for category in categories:
            categories_card.controls.append(
                Container(
                    bgcolor='#041955', height=100, width=130,
                    border_radius=20,padding=15,
                    content=Column(
                        controls=[
                            Text('40 Tasks', color='white'),
                            Text(category, color='white'),
                            Container(
                                width=120,
                                height=5,
                                bgcolor="white12",
                                border_radius=20,
                                padding=padding.only(right=10),
                                content=Container(
                                    bgcolor=self.PINK
                                )
                            )
                        ]
                    )
                )
            )

        # 定义任务

        tasks = Column(
            scroll=ScrollMode.AUTO,
            width=self.page.width-40,
            height=250,
            controls=[
                Container(
                    height=40, width=self.page.width-40, bgcolor="#041955", border_radius=20,
                    content=ft.Container(ft.Checkbox(label="测试仪嘻嘻嘻嘻嘻", label_style=TextStyle(color="white"), hover_color="white12"))
                ),
                Container(
                    height=40, width=self.page.width-40, bgcolor="#041955", border_radius=20,
                    content=ft.Container(ft.Checkbox(label="测试仪嘻嘻嘻嘻嘻", label_style=TextStyle(color="white"), hover_color="white12"))
                ),
                Container(
                    height=40, width=self.page.width-40, bgcolor="#041955", border_radius=20,
                    content=ft.Container(ft.Checkbox(label="测试仪嘻嘻嘻嘻嘻", label_style=TextStyle(color="white"), hover_color="white12"))
                ),
                Container(
                    height=40, width=self.page.width-40, bgcolor="#041955", border_radius=20,
                    content=ft.Container(ft.Checkbox(label="测试仪嘻嘻嘻嘻嘻", label_style=TextStyle(color="white"), hover_color="white12"))
                ),
                Container(
                    height=40, width=self.page.width-40, bgcolor="#041955", border_radius=20,
                    content=ft.Container(ft.Checkbox(label="测试仪嘻嘻嘻嘻嘻", label_style=TextStyle(color="white"), hover_color="white12"))
                ),
                Container(
                    height=40, width=self.page.width-40, bgcolor="#041955", border_radius=20,
                    content=ft.Container(ft.Checkbox(label="测试仪嘻嘻嘻嘻嘻", label_style=TextStyle(color="white"), hover_color="white12"))
                ),
            ]
        )


        def shrink(e):
            "页面向右缩放的函数，就是通过控制组件的参数实现"
            self.page2.controls[0].width = 100
            self.bgcolor = '#041955'
            self.page2.controls[0].scale = transform.Scale(
                0.8, alignment=alignment.center_right
            )
            self.page2.alignment = "end"
            self.page2.controls[0].on_click = lambda _: restore(_)
            self.page.update()
        
        def restore(e):
            print("出发了")
            self.page2.controls[0].width = None
            self.bgcolor = '#3450a1'
            self.page2.controls[0].scale = transform.Scale(
                1, alignment=alignment.center_right
            )
            self.page2.alignment = None
            self.page2.controls[0].on_click = None
            self.page.update()

        first_page_contents = Container(
            width=self.page.width-40,
            content=Column(controls=[
                Container(height=10),
                Row(
                    alignment="spaceBetween",
                    controls=[
                        Container(content=Icon(name=icons.MENU, color="white"),
                                  on_click=lambda _: shrink(_)),
                        Row(controls=[
                            Icon(icons.SEARCH, color="white"),
                            Icon(icons.NOTIFICATIONS_OUTLINED, color="white"),
                        ]),    
                    ],
                    height=40
                ),
                Text(value="今日进度", size=25, color="white"),
                Text(value="分类", color="white"),
                Container(
                    content=categories_card
                ),
                Container(height=20),
                Text(value="今日待办", size=25, color="white"),
                # 这里用Stack是为了让悬浮弹窗能够显示在上面
                Stack(
                   
                    controls=[
                        tasks, 
                        FloatingActionButton(
                            bottom=2, right=20,
                            icon=icons.ADD,
                            on_click=lambda _: page.go('/create_task'))
                    ]
                )
            ])
        )

        self.page1 = Container(
            border_radius=35,
            padding=padding.only(left=40, top=60, right=200),
            content=Text(value="???", color="white"),
            on_click=lambda _ : restore(_)
        )

        self.page2 = Row(
            # 这里设置alignment="end",能够实现当页面缩放的时候，组件是靠右缩放的
            controls=[Container(
                border_radius=20,
                bgcolor='#3450a1',
                animate=animation.Animation(600, AnimationCurve.DECELERATE),
                animate_scale=animation.Animation(400, AnimationCurve.DECELERATE),
                content=first_page_contents,
                # bgcolor='#041955'
            )]
        )

        self.controls = [
            Stack(
                controls=[
                    self.page1,
                    self.page2
                ],
            )
        ]

def main(page: Page):
    
    def router(router):
        page.views.clear()
        if page.route == '/':
            index_page = Index(page)
            page.views.append(index_page)
        elif page.route == '/create_task':
            create_task_page = CreateTask(page)
            page.views.append(create_task_page)
        page.update()
    
    page.on_route_change = router
    page.go('/')
    pass

app(target=main)
