from src.SpeechToText import SpeechToTextModule
from src.TextToSpeech import TextToSpeechModule

from abc import ABCMeta, abstractmethod
import json


class ParentClassForModules():
    """Родительский класс, обязательный для наследования всеми модулями на реализацию."""

    def __init__(self, name: str, stt: SpeechToTextModule, tts: TextToSpeechModule):
        self.name = name
        self.stt = stt
        self.tts = tts
        self.commands = {}

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def info(self) -> str:
        pass
