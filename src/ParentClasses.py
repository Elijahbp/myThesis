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
            'name_ru': '',
            'version': '',
        }

    @abstractmethod
    def load_commands(self):
        pass

    #abstractmethod
    def command_analyzer(self, input_command: str) -> list:
        """
            Анализатор входной команды, для определения, какой функционал необходимо исполнять
            :return - разбитую команду (list),
        """
        #1) разделяем команду
        #2) по словно проходимся по имеющимся командам
        #3) Если совпадение >1 - продолжаем поиск по совпадениям
        #              если =1 - совпадение команды (стоит ли делать проверку полной целлостности комманды???)
        #              если =0 - совпадений нет - Exception (?)

        #for key_words, structure in self.commands.items():
        return


    @abstractmethod
    def run_command(self, structure: dict, args: list):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def info(self) -> str:
        output_info = "Модуль: " + self.info_str['name_ru'] + " Версия: " + self.info_str['version']
        # self.tts.say(output_info)
        return output_info
