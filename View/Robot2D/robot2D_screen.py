from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial

from View.Robot2D.components import CardProfile  # NOQA
from View.Robot2D.components import CardMessage  # NOQA
from View.Robot2D.components import CardCall  # NOQA
from View.Robot2D.components import CardNotification  # NOQA

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

import matplotlib
import math as Math
import numpy as np
import time

# Define what we want to graph
x = [1, 2, 3, 4, 5]
y = [5, 12, 6, 9, 15]

plt.plot(x, y)
plt.ylabel("This is MY Y Axis")
plt.xlabel("X Axis")


class Robot2DView(MDScreen):
    # les boutons
    data = {
        "  Demo    ": "robot",
        "Dessiner": "draw",
        "Simuler": "robot-industrial-outline",
        'Nouveau': [
            'new-box',
            "on_press", lambda x: print("pressed C++"),
            "on_release", lambda x: print("OKOK")
        ],
    }

    # Base de données des valeurs par défaut
    DonneDefaut = {
        "LongeurL0": 3.5,
        "LongeurL1": 3,
        "LongeurL2": 3,
        "Angle1": 55,
        "Angle2": 75,
        "AbsB": 0,
        "OrdB": 1,
        "NombrePas": 10,
        "DuréeTrajet": 15
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        box = self.ids.box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def do_layout(self):
        pass
        # fenetreC11.grid(row=1, column=1, sticky="nsew")
        # fenetreC12.grid(row=2, column=1, sticky="nsew")
        # fenetreC21.grid(row=1, column=2, sticky="nsew")
        # fenetreC22.grid(row=2, column=2, sticky="nsew")
        #
        # fenetre.grid_rowconfigure(1, weight=1)
        # fenetre.grid_columnconfigure(0, weight=1)
        # fenetre.grid_rowconfigure(1, weight=1)
        # fenetre.grid_columnconfigure(1, weight=1)
        # fenetre.grid_rowconfigure(1, weight=1)
        # fenetre.grid_columnconfigure(2, weight=1)
        # fenetre.grid_rowconfigure(2, weight=1)
        # fenetre.grid_columnconfigure(0, weight=1)
        # fenetre.grid_rowconfigure(2, weight=1)
        # fenetre.grid_columnconfigure(1, weight=1)
        # fenetre.grid_rowconfigure(2, weight=1)
        # fenetre.grid_columnconfigure(2, weight=1)

    def _quit(self):
        pass
        # fenetre.quit()
        # fenetre.destroy()
