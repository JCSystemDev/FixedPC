import pywhatkit
import datetime
import time


def enviar_mensaje_despues(mensaje, hora, minuto):
    # Enviar el mensaje
    pywhatkit.sendwhatmsg("+56958997028", mensaje, hora, minuto)
