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
        self.info_str = {
            'name_ru':'',
            'version':'',
        }

    @abstractmethod
    def command_analyzer(self, command: str):
        pass

    @abstractmethod
    def run_command(self, id: int, **kwargs):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def info(self) -> str:
        output_info = "Модуль: " + self.info_str['name_ru'] + " Версия: " + self.info_str['version']
        #self.tts.say(output_info)
        return output_info
