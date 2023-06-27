import pywhatkit
import datetime


def obtener_hora_actual():
    hora_actual = datetime.datetime.now()
    print(hora_actual)
    return hora_actual


def enviar_notificacion(contact, message, hora, minuto):
    pywhatkit.sendwhatmsg(contact, message, hora, minuto)
