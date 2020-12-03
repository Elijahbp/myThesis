from src.SpeechToText import SpeechToTextModule
from src.TextToSpeech import TextToSpeechModule

import json

class ParentClassForModules():
    """Родительский класс, обязательный для наследования всеми модулями на реализацию."""
    def __init__(self, name: str, stt: SpeechToTextModule, tts: TextToSpeechModule):
        self.name = name
        self.stt = stt
        self.tts = tts
        self.commands = {}

    #обязательные методы! - init, stop