import pywhatkit


def enviar_mensaje_despues(numero, mensaje, hora, minuto):
    # Enviar el mensaje
    pywhatkit.sendwhatmsg(numero, mensaje, hora, minuto)
