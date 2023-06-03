from random import choice
from flet import *
import flet as ft
from Bard import Chatbot

h = 1080
w = 720

token = 'token'

bot = Chatbot(token)

page1col = '#303030'
page2col = '#303030'
page3col = '#303030'
sidebarcol = '#454545'
logocol = 'white'


class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.BLACK,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=1,
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


class App(UserControl):
    def __init__(self, pg):
        super().__init__()
        # pg.bgcolor = colors.TRANSPARENT
        # pg.window_bgcolor = colors.TRANSPARENT
        # pg.window_title_bar_hidden =True
        # pg.window_frameless = True
        self.pg = pg
        self.animation_style = animation.Animation(600, AnimationCurve.DECELERATE)

        self.init_helper()

    def init_helper(self):
        self.side_bar_column = Column(
            spacing=0,
            controls=[
                Row(
                    controls=[
                        Container(
                            data=0,
                            on_click=lambda e: self.switch_page(e, 'page1'),
                            expand=True,
                            height=80,
                            content=Icon(
                                icons.CHAT_BUBBLE,
                                color=logocol
                            ),
                        ),
                    ]
                ),

                Row(
                    controls=[
                        Container(
                            on_click=lambda e: self.switch_page(e, 'page2'),
                            data=1,
                            expand=True,
                            height=80,
                            content=Icon(
                                icons.BADGE,
                                color=logocol
                            ),
                        ),
                    ]
                ),

                Row(
                    controls=[
                        Container(
                            expand=True,
                            height=80,
                            data=2,
                            on_click=lambda e: self.switch_page(e, 'page3'),
                            content=Icon(
                                icons.SETTINGS,
                                color=logocol
                            ),
                        ),
                    ]
                ),

            ]
        )

        self.indicator = Container(
            height=80,
            bgcolor='red',
            offset=transform.Offset(0, 0),
            animate_offset=animation.Animation(600, AnimationCurve.DECELERATE)
        )

        new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
        )

        chat = ft.ListView(
            expand=True,
            spacing=20,
            auto_scroll=True,
        )

        # A new message entry form
        def send_click(e):
            if new_message.value != "":
                self.page1.page.pubsub.send_all(
                    Message(self.pg.session.get("user_name"), new_message.value, message_type="chat_message"))

                if "bard" in new_message.value.lower():
                    bard = bot.ask(new_message.value)['content']
                    chat.controls.append(ft.Text("BARD: " + bard))

                new_message.value = ""
                new_message.focus()
                self.page1.update()

            if username.value == "":
                chat.controls.append(ft.Text("Type A Username first"))
                self.page1.update()

        def on_message(message: Message):
            if message.message_type == "chat_message":
                m = ChatMessage(message)
            elif message.message_type == "login_message":
                m = ft.Text(message.text, italic=True, color=ft.colors.WHITE, size=12)
            chat.controls.append(m)
            self.page1.update()

        self.pg.pubsub.subscribe(on_message)

        self.page1 = Container(
            offset=transform.Offset(0, 0),
            content=Column(
                controls=[
                    chat,
                    Row(
                        controls=[
                            new_message,
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_click,

                            ),
                        ],
                    ),
                ],
            ),
            expand=True,
            bgcolor=page1col,
        )

        # page 2 functuions
        self.page2 = Container(
            alignment=alignment.center,
            offset=transform.Offset(0, 0),
            animate_offset=self.animation_style,
            bgcolor=page2col,
        )

        username = ft.TextField(
            hint_text="Write a username",
            autofocus=True,
            shift_enter=False,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=False,
        )

        def username_click(e):
            if not username.value:
                username.error_text = "Name cannot be blank!"
                username.update()
            else:
                self.pg.session.set("user_name", username.value)
                new_message.prefix = ft.Text(f"{username.value}: ")
                self.page1.page.pubsub.send_all(
                    Message(user_name=username.value, text=f"{username.value} has joined the chat.",
                            message_type="login_message"))
                self.switch_page(e, 'page1')
                self.page1.update()

        Userbutton = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
            tooltip="Send message",
            on_click=username_click
        )

        self.page3 = Container(
            alignment=alignment.center,
            offset=transform.Offset(0, 0.0),
            animate_offset=self.animation_style,
            bgcolor=page3col,
            content=Row(controls=[username, Userbutton]),
        )

        self.switch_control = {
            'page1': self.page1,
            'page2': self.page2,
            'page3': self.page3,
        }

        self.pg.add(
            Container(
                bgcolor=sidebarcol,
                expand=True,
                content=Row(
                    spacing=0,
                    controls=[
                        Container(
                            width=80,
                            # bgcolor='green',
                            border=border.only(right=border.BorderSide(width=1, color='black'), ),
                            content=Column(
                                alignment='spaceBetween',
                                controls=[

                                    Container(
                                        height=100,
                                        # bgcolor='blue'
                                    ),

                                    Container(
                                        height=500,
                                        content=Row(
                                            spacing=0,
                                            controls=[
                                                Container(
                                                    expand=True,
                                                    content=self.side_bar_column,

                                                ),
                                                Container(
                                                    width=3,
                                                    content=Column(
                                                        controls=[
                                                            self.indicator,
                                                        ]
                                                    ),

                                                ),
                                            ]
                                        )
                                    ),

                                    Container(
                                        height=50,
                                    ),
                                ]
                            )
                        ),

                        Container(
                            expand=True,
                            content=Stack(
                                controls=[
                                    self.page1,
                                    self.page2,
                                    self.page3,

                                ]
                            )
                        ),
                    ]
                )

            )
        )

    def switch_page(self, e, point):
        print(point)
        for page in self.switch_control:
            self.switch_control[page].offset.x = 2
            self.switch_control[page].update()

        self.switch_control[point].offset.x = 0
        self.switch_control[point].update()

        self.indicator.offset.y = e.control.data
        self.indicator.update()


app(target=App, assets_dir='assets', view=ft.WEB_BROWSER)
