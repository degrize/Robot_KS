import hashlib
import sqlite3

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import StencilBehavior


class Connexion(MDScreen, StencilBehavior):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.app = MDApp.get_running_app()
        self.cursor = None
        self.connexion = None
        self.connexionDB()

    def connexionDB(self):
        try:
            self.connexion = sqlite3.connect("base_donnees/robot_ks.db")
            self.cursor = self.connexion.cursor()

        except Exception as e:
            print("[ERREUR] ", e)

    def authentification(self):
        login = self.ids.login_field.text + ''
        pwd = self.ids.password_field.text + ''

        utilisateur = (login, pwd)
        req = self.cursor.execute('SELECT * FROM robot_utilisateur WHERE login = ? and password = ?', utilisateur)

        if req.fetchall():
            self.app.manager_screen.switch_screen("robot2D")
        else:
            self.ids.label_infoConexion.text = "Mot de passe incorrect"

        auth = pwd.encode()
        auth_hash = hashlib.md5(auth).hexdigest()


