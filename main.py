import os
import sys
from pathlib import Path

from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles
from kivymd.theming import ThemableBehavior

from View.ManagerScreen.manager_screen import ManagerScreen

import sqlite3



if getattr(sys, "frozen", False):
    os.environ["ROBOT_KS_ROOT"] = sys._MEIPASS
else:
    sys.path.append(os.path.abspath(__file__).split("demos")[0])
    os.environ["ROBOT_KS_ROOT"] = str(Path(__file__).parent)
os.environ["ROBOT_KS_ASSETS"] = os.path.join(
    os.environ["ROBOT_KS_ROOT"], f"assets{os.sep}"
)
Window.softinput_mode = "below_target"


class RobotMain(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Robotiques"
        self.description = "Le projet de robotique ING-2"
        self.icon = "assets/images/logo.png"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.accent_palette = "Teal"

        theme_font_styles.append('JetBrainsMono')
        self.theme_cls.font_styles["JetBrainsMono"] = [
            "JetBrainsMono",
            16,
            False,
            0.15,
        ]

        self.manager_screen = ManagerScreen()

    def build(self) -> ManagerScreen:
        # self.manager_screen.add_widget(self.manager_screen.create_screen("menu"))
        self.manager_screen.add_widget(self.manager_screen.create_screen("robot2D"))
        return self.manager_screen

    def blackwhit(self):

        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "Gray"
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Orange"


RobotMain().run()
