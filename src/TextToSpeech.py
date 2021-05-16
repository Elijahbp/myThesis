import pyttsx3


class TextToSpeechModule():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 250)
        self.engine.setProperty('volume', 0.7)

    def say(self, msg: str):
        self.engine.say(msg)
        self.engine.runAndWait()
        print(msg)
