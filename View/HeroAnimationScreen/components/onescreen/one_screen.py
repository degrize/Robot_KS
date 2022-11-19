from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.screen import MDScreen

from View.HeroAnimationScreen.components import CityCard


class OneScreenView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_enter(self):
        if not self.ids.box.children:
            for name_image in [
                "Huawei", "BostonDynamique", "Tesla", "Nvidia","Huawei", "BostonDynamique", "Tesla",
            ]:
                card = CityCard(
                    source=f"assets/images/hero_screen/{name_image}.jpg",
                    tag=name_image,
                    size_hint_y=None,
                    height="200dp",
                )
                card.ids.tile.bind(on_release=self.on_tap_city_card)
                self.ids.box.add_widget(card)

    def on_tap_city_card(self, tile: MDSmartTile) -> None:
        def switch_screen(*args):

            try:
                self.app.description = tile.parent.tag
                print(self.app.description)
                self.manager.current_hero = tile.parent.tag
                self.manager.current = "hero two screen"
            except:
                pass

        Clock.schedule_once(switch_screen, 0.1)

    def back_to_menu(self):
        MDApp.get_running_app().manager_screen.current = "menu"
