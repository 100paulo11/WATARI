import pyttsx3


class VozWatari:

    def __init__(self, velocidade=180, volume=1.0):
        self.motor = pyttsx3.init()
        self.motor.setProperty("rate", velocidade)
        self.motor.setProperty("volume", volume)

    def falar(self, mensagem):
        print(f"Watari: {mensagem}")
        self.motor.say(mensagem)
        self.motor.runAndWait()
