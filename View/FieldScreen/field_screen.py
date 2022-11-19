from kivymd.theming import ThemableBehavior
from kivymd.uix.screen import MDScreen

from View.FieldScreen.components import OneScreen  # NOQA
from View.common.round_card import RoundCard  # NOQA

from View.slide_animatior import SlideAnimatior


class FieldScreenView(ThemableBehavior, MDScreen, SlideAnimatior):
    pass
