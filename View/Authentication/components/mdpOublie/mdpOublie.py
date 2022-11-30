from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import StencilBehavior

from View.common.rectangular_card import RectangularCard  # NOQA

import smtplib
import ssl
from email.message import EmailMessage


class MdpOublieView(MDScreen, StencilBehavior):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.email_receiver = None
        self.email_sender = "mdegrize@gmail.com"
        self.email_password = "owvudcwpuglqcwmg"
        self.subject = "Recuperation du mot de passe"
        self.body = """
                    LES IDENTIFIANT DE CONNEXION À L'APPLICATION :
                    
                            Login : meda
                            Mot de passe: 1234
                    """

    def sendMail(self):
        if self.verificationSaisie():
            em = EmailMessage()
            em['From'] = self.email_sender
            em['To'] = self.email_receiver
            em['Subject'] = self.subject
            em.set_content(self.body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.sendmail(self.email_sender, self.email_receiver, em.as_string())
                self.ids.label_infoConexion.opacity = 1
                self.ids.label_infoConexion.text = "Le mail a bien été envoyé"
                self.ids.label_infoConexion.text_color = "green"
                self.ids.email_field.text = ""

                return True

    def verificationSaisie(self):

        if not self.ids.email_field.error:
            self.email_receiver = self.ids.email_field.text
            return True

        self.ids.label_infoConexion.opacity = 1
        self.ids.label_infoConexion.text = "Le mail n'a pas été envoyé"
        self.ids.label_infoConexion.text_color = "red"

    def clearField(self):
        self.ids.label_infoConexion.text = ""
        self.ids.label_infoConexion.opacity = 0
