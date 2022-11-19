import os

from kivymd.uix.screen import MDScreen

from View.MenuScreen.componemts import MenuCard  # NOQA


class MenuScreenView(MDScreen):
    def on_enter(self, *args) :
        print(33)
