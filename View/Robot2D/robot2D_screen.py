from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.utils import asynckivy

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


#
# plt.plot(x, y)
# plt.ylabel("This is MY Y Axis")
# plt.xlabel("X Axis")


class Robot2DView(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.restartSimulator = False
        """  Nous faisons correspondre nos attributs class a son champs  """
        self.dureeTrajetAB = self.ids.setting.ids.dureeTrajetAB
        self.nbrePas = self.ids.setting.ids.nbrePas
        self.ordB = self.ids.setting.ids.ordB
        self.absB = self.ids.setting.ids.absB
        self.Ɵ2 = self.ids.setting.ids.Ɵ2
        self.Ɵ1 = self.ids.setting.ids.Ɵ1
        self.L2 = self.ids.setting.ids.L2
        self.L1 = self.ids.setting.ids.L1
        self.btnData = None
        self.L0 = self.ids.setting.ids.L0

        # On prepare notre graphe
        self.settingMatplotLib()

    def calculMatricesPassage(self):
        if self.verifAllFieldsCorrect():
            L00 = float(self.L0.text)
            L11 = float(self.L1.text)
            L22 = float(self.L2.text)

            if L00 >= 7 or L11 >= 7 or L22 >= 7:
                print("verifier L0 - L1 & L2")
                return

            O11 = Math.radians(float(self.Ɵ1.text))
            O22 = Math.radians(float(self.Ɵ2.text))
            nbrePas = int(self.nbrePas.text)
            YB = float(self.ordB.text)  # la valeur d'ordonnées de B
            XB = float(self.absB.text)  # la valeur d'abscisse de B

            if YB >= 7 or XB >= 7:
                print("verifier YB & XA")
                return

            # LES MATRICES DE PASSAGE DIRECTE
            Mat0T1 = np.array([
                [Math.cos(O11), -Math.sin(O11), 0, L00],
                [Math.sin(O11), Math.cos(O11), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
            Mat1T2 = np.array([[Math.cos(O22), -Math.sin(O22), 0, L11],
                               [Math.sin(O22), Math.cos(O22), 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
            Mat0T2 = Mat0T1.dot(Mat1T2)
            A2 = np.array([[L22],
                           [0],
                           [0],
                           [1]])
            A21 = np.array([[L11],
                            [0],
                            [0],
                            [1]])
            A10 = np.array([[L00],
                            [0],
                            [0],
                            [1]])
            A0 = Mat0T2.dot(A2)
            A20 = Mat0T1.dot(A21)
            # notre angle de rotation de 0A2
            rotAngle = Math.degrees(Math.atan2(Mat0T2[[1], [0]], Mat0T2[[0], [0]]))
            # Le cas les matrices de passage inverse
            Mat1T0 = np.array([[Math.cos(O11), Math.sin(O11), 0, -L00 * Math.cos(O11)],
                               [-Math.sin(O11), Math.cos(O11), 0, L00 * Math.sin(O11)],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

            Mat2T1 = np.array([[Math.cos(O22), Math.sin(O22), 0, -L00 * Math.cos(O22)],
                               [-Math.sin(O22), Math.cos(O22), 0, L11 * Math.sin(O22)],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

            return [nbrePas, L00, A20, A0, YB, XB, L11, L22]

        return False

    def showRobot(self):
        self.verif = False
        self.restartSimulator = True
        self.plot.cla()
        self.plot.set_xlabel('Y0')
        self.plot.set_ylabel('X0')
        self.plot.yaxis.set_ticks_position('right')
        self.plot.set_xticks(range(8))
        self.plot.set_yticks(range(8))
        self.plot.set_xlim((8, -1))
        self.plot.set_ylim((-1, 8))

        result = self.calculMatricesPassage()
        if not result:
            return

        L00 = result[1]
        A20 = result[2]
        A0 = result[3]
        YB = result[4]
        XB = result[5]
        nbreMaxPas = result[0]

        if ((A0[1] - XB) ** 2 + (A0[0] - YB) ** 2) ** 0.5 > result[6] + result[7] or (
                (A0[1] - XB) ** 2 + (A0[0] - YB) ** 2) ** 0.5 < abs(result[6] - result[7]):
            return

        if ((A20[1] - 0) ** 2 + (A20[0] - 0) ** 2) ** 0.5 > 7:
            return

        self.plot.plot([0.0, 0.0], [0.0, L00], "b-", lw=7)
        self.plot.plot([0.0, A20[1]], [L00, A20[0]], "b-", lw=7)
        self.plot.plot([A20[1], A0[1]], [A20[0], A0[0]], "b-", lw=7)

        self.plot.scatter([A0[1]], [A0[0]], s=500, color='red')
        self.plot.scatter([YB], [XB], s=500, color='red')

        self.plot.scatter([0.0], [L00], s=500, color='black')
        self.plot.scatter([A20[1]], [A20[0]], s=500, color='black')

        self.plot.plot([-0.5, 0.5], [0.0, 0.0], "k-", lw=10)
        self.plot.plot([0.0, 7.0], [0.0, 0.0], "k", marker='<', markersize=15, lw=3)
        self.plot.plot([0.0, 0.0], [0.0, 7.0], "k", marker='^', markersize=15, lw=3)
        self.graphique.draw()

    def simulateRobot(self):

        """
            Dans cette methode nous simulons notre robot, le bras du robot se déplacera jusqu'au point B
        """

        async def simulateRobot():

            etatBtnPas = True
            etatBtnBip = True
            etatBtnR0 = True
            etatBtnTrajectoire = True
            X_Pi = []
            Y_Pi = []

            if self.nbrePas.text == "":
                return

            if self.dureeTrajetAB.text == "":
                return

            result = self.calculMatricesPassage()
            if not result:
                return
            nbrePas = int(self.nbrePas.text)
            L0 = result[1]
            L1 = result[6]
            L2 = result[7]
            YB = result[4]
            A0 = result[3]
            XB = result[5]
            A20 = result[2]
            vitesse = float(self.dureeTrajetAB.text) / nbrePas
            self.restartSimulator = not self.restartSimulator
            for i in range(1, nbrePas + 1):
                self.plot.cla()
                # Définir les propriétés du restartSimulator graph
                self.plot.set_xlabel('Y0')
                self.plot.set_ylabel('X0')
                self.plot.yaxis.set_ticks_position('right')
                self.plot.set_xticks(range(8))
                self.plot.set_yticks(range(8))
                self.plot.set_xlim((8, -1))
                self.plot.set_ylim((-1, 8))
                self.plot.plot([0.0, 7.0], [0.0, 0.0], "k", marker='<', markersize=15, lw=3)
                self.plot.plot([0.0, 0.0], [0.0, 7.0], "k", marker='^', markersize=15, lw=3)
                # self.plot.set_axis_off()
                # self.plot.grid(True)

                # Distance X entre deux pas
                disXPas = (XB - A0[0]) / nbrePas
                if disXPas < 0:
                    disXPas = -disXPas
                # Distances-Y entre deux pas
                disYPas = (YB - A0[1]) / nbrePas
                if disYPas < 0:
                    disYPas = -disYPas
                if XB >= A0[0]:
                    Xi = A0[0] + i * disXPas
                else:
                    Xi = A0[0] - i * disXPas

                if YB > A0[1]:
                    Yi = A0[1] + i * disYPas
                else:
                    Yi = A0[1] - i * disYPas

                # LES CALCULS ------------------------------------->

                B1 = -2 * Yi * L1
                B2 = 2 * L1 * (L0 - Xi)
                B3 = L2 ** 2 - Yi ** 2 - (L0 - Xi) ** 2 - L1 ** 2
                teta_1 = 0
                teta_2 = 0
                SO1 = 0
                CO1 = 0
                epsi = 1
                if B3 == 0:
                    teta_1 = Math.degrees(Math.atan2(-B2, B1))
                else:
                    if (B1 ** 2 + B2 ** 2 - B3 ** 2) >= 0:
                        SO1 = (B3 * B1 + epsi * B2 * Math.sqrt(B1 ** 2 + B2 ** 2 - B3 ** 2)) / (B1 ** 2 + B2 ** 2)
                        CO1 = (B3 * B2 - epsi * B1 * Math.sqrt(B1 ** 2 + B2 ** 2 - B3 ** 2)) / (B1 ** 2 + B2 ** 2)
                        teta_1 = Math.degrees(Math.atan2(SO1, CO1))
                    else:
                        break
                Yn1 = L2 * SO1
                Yn2 = L2 * CO1

                if L2 != 0:
                    teta_2 = Math.degrees(Math.atan2(Yn1 / L2, Yn2 / L2))
                else:
                    break
                XA1i = L1 * Math.cos(Math.radians(teta_1)) + L0
                YA1i = L1 * Math.sin(Math.radians(teta_1))


                # Trajectoire
                if etatBtnTrajectoire:
                    XA0 = result[3][0]
                    XB = result[5]
                    YA0 = result[3][1]
                    YB = result[4]
                    a = (YA0 - YB) / (XA0 - XB)
                    b = YB - a * XB
                    x = range(-100, 101)  # ,nbrePas)
                    y = a * x + b
                    # Trace la droite
                    # self.plot.plot(y,x,"k-",lw=3)
                    # Droite entre A et Pi
                    # self.plot.plot([A0[1],Yi],[A0[0],Xi],"y-",lw=5)

                # sauvegarde-les coordonnées des Pi
                X_Pi.append(Xi)
                Y_Pi.append(Yi)

                # Les Pas
                if etatBtnPas:
                    for j in range(0, len(X_Pi)):
                        self.plot.scatter([Y_Pi[j]], [X_Pi[j]], s=200, color='#3dd9c1')

                # for j in range(0,X_Pi.len()):
                #   print(X_Pi, Y_Pi)
                # tracer L0

                self.plot.plot([0.0, 0.0], [0.0, L0], "b-", lw=7)
                # tracer L1
                self.plot.plot([0.0, YA1i], [L0, XA1i], "b-", lw=7)
                # tracer L2
                self.plot.plot([YA1i, Yi], [XA1i, Xi], "b-", lw=7)
                # Point Pi
                self.plot.scatter([Yi], [Xi], s=500, color='#FF0000')
                # Point A0
                self.plot.scatter([0], [L0], s=500, color='black')
                # Point A2
                self.plot.scatter([YA1i], [XA1i], s=500, color='black')
                if i != 0:
                    # Le point A
                    self.plot.scatter([A0[1]], [A0[0]], s=300, color='#006633')
                else:
                    # Le point A
                    self.plot.scatter([A0[1]], [A0[0]], s=500, color='#FF0000')
                if i == nbrePas:
                    # Le point B
                    self.plot.scatter([YB], [XB], s=300, color='#FF0000')
                else:
                    # Le point B
                    self.plot.scatter([YB], [XB], s=300, color='#00FF33')

                # Le repere R0
                """
                tatBtnR0=True
                if etatBtnR0==True:
                    self.plot.plot([0.0,0.0],[0.0,15.0],"r-",lw=2)
                    self.plot.plot([0.0,15.0],[0.0,0.0],"r-",lw=2)
                #Le repere R1
                etatBtnR1=True
                if etatBtnR1==True:
                    m=(YA1i-0)/(XA1i-L0)
                    c=YA1i-m*XA1i
                    u = m*(16)+c
                    self.plot.plot([0.0,u],[L0,16.0],"y--",lw=2)
                    l = (-1/m)*(16)+YA1i+(1/m)*XA1i
                    self.plot.plot([0.0,l],[L0,16.0],"y--",lw=2)
                #Le repere R2
                etatBtnR2=True
                if etatBtnR2==True:
                    m=(YA1i-Yi)/(XA1i-Xi)
                    c=YA1i-m*XA1i
                    u = m*16+c
                    self.plot.plot([YA1i,u],[XA1i,16.0],"m--",lw=2)
                    l = (-1/m)*(-16)+YA1i+(1/m)*XA1i
                    self.plot.plot([YA1i,l],[XA1i,-16.0],"m--",lw=2)
                """
                # Le sol
                self.plot.plot([-0.5, 0.5], [0.0, 0.0], "k-", lw=10)
                self.plot.plot([0.0, 5.0], [0.0, 0.0], "k--", lw=3)

                # self.plot.grid(True)
                await asynckivy.sleep(vitesse)
                self.graphique.draw()

                self.verif = True
                if self.restartSimulator:
                    return

                """
                if etatBtnBip==True:
                    #Le Bip
                    winsound.Beep(440, 250)
                """

        asynckivy.start(simulateRobot())

    def verifAllFieldsCorrect(self):
        """
            On vérifie si l'utilisateur a bien renseigné les champs
        :return:
        """
        if (self.L0.text and self.L1.text and self.L2.text and self.Ɵ1.text and self.Ɵ2.text
                and self.ordB.text and self.absB.text and self.dureeTrajetAB.text):  # si tout est renseigné alors
            return True

        print("VERIFIER VOS SAISIES")

        self.L1.focus = True
        self.L1.required = True
        self.L2.focus = True
        self.L2.required = True

        self.Ɵ1.focus = True
        self.Ɵ1.required = True
        self.Ɵ2.focus = True
        self.Ɵ2.required = True

        self.absB.focus = True
        self.absB.required = True
        self.ordB.focus = True
        self.ordB.required = True

        self.nbrePas.focus = True
        self.nbrePas.required = True
        self.dureeTrajetAB.focus = True
        self.dureeTrajetAB.required = True

        self.L0.focus = True
        self.L0.required = True

        return False

    def settingMatplotLib(self):
        self.restartSimulator = True

        self.fig = plt.figure()
        self.plot = self.fig.add_subplot(1, 1, 1)

        self.plot.yaxis.set_ticks_position('right')
        self.plot.set_xticks(range(10))
        self.plot.set_yticks(range(10))
        self.plot.set_xlim((10, -1))
        self.plot.set_ylim((-1, 10))
        self.plot.grid(True)

        self.graphique = FigureCanvasKivyAgg(plt.gcf())
        self.graphique.draw()

        """ Nous affichons notre GRAPHE """
        box = self.ids.box
        box.clear_widgets()
        box.add_widget(self.graphique)

    # les boutons
    def btn_layout(self):
        self.btnData = {
            "  Demo    ": [
                'robot',
                "on_release", lambda x: self.defaultSetting()
            ],
            "Dessiner": [
                'draw',
                "on_release", lambda x: self.showRobot()
            ],
            "Simuler": [
                'robot-industrial-outline',
                "on_release", lambda x: self.simulateRobot()
            ],
            'Nouveau': [
                'new-box',
                "on_press", lambda x: print("pressed C++"),
                "on_release", lambda x: self.clearAllField()
            ],
        }
        return self.btnData

    # Base de données des valeurs par défaut
    def defaultSetting(self):

        self.L0.text = str(3.5)
        self.L1.text = str(3)
        self.L2.text = str(3)
        self.Ɵ1.text = str(55)
        self.Ɵ2.text = str(75)
        self.absB.text = str(0)
        self.ordB.text = str(1)
        self.nbrePas.text = str(10)
        self.dureeTrajetAB.text = str(4)

    def clearAllField(self):
        self.L0.text = ""
        self.L1.text = ""
        self.L2.text = ""
        self.Ɵ1.text = ""
        self.Ɵ2.text = ""
        self.absB.text = ""
        self.ordB.text = ""
        self.nbrePas.text = ""
        self.dureeTrajetAB.text = ""

        self.settingMatplotLib()
