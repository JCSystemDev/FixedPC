import pywhatkit
# pywhatkit es una biblioteca de python que permite diferentes funcionalidades, entre ellas el enviar mensajes por whatsapp

def enviar_mensaje_despues(numero, mensaje, hora, minuto):
    # Enviar el mensaje
    pywhatkit.sendwhatmsg(numero, mensaje, hora, minuto)
