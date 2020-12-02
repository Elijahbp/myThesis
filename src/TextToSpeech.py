import pyttsx3

class TextToSpeechModule():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate',150)
        self.engine.setProperty('volume',0.9)



    def say(self,msg:str):
        self.engine.say(msg)
        self.engine.runAndWait()