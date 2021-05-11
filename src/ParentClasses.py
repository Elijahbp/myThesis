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
        self.dictionary_of_arguments = {}
        self.info_str = {
            'name_ru': '',
            'version': '',
        }

    @abstractmethod
    def load_commands(self):
        pass

    def analyze_command_and_run(self, input_data: str):
        if input_data == '':
            self.tts.say('Команда не распознана. Повторите пожалуйста!')
            return None
        command_data = []
        command_data = self.get_structure_input_data(input_data=input_data)
        if not command_data:
            return None
        key_word = command_data[0].lower()  # TODO: Страшная условность - необходимо переосмыслить!!!
        # TODO ПЕРЕРАБОТАТЬ
        for key_words, structure in self.commands.items():
            if key_word in key_words:
                self.run_command(structure, command_data)
                return True
        else:
            return False

    @abstractmethod
    def run_command(self, parse_data: dict):
        pass

    def get_structure_input_data(self, input_data: str) -> dict:
        # правило для определения кол-ва параметров
        # 1) Определение слов команд
        # 2) определение слов аргументов
        # 3) вычленение аргументов
        # команды всегда идут в начале!
        # структура сетов:
        # "sets":{
        # "1":{
        #   "args": [],
        #   "data": []
        # }
        # "2":{
        #   "args": [],
        #   "data": []
        # }
        # }
        parse_data = {
            "command": None,
            "sets": {}
        }
        # парсим входную строку
        input_data = input_data.split(' ')
        # проверяем на комманды
        structure = {}
        count_word = 0
        for word in input_data:
            count_word += 1
            if not structure:
                for key, value in self.commands.items():
                    # получаем перечень слов, которые были затригерены, и могут быть частью вводимой комманды
                    triggered_words = list(filter(lambda x: word.lower() in x, value['trigger_words']))
                    if triggered_words:
                        # получаем словосочетание, затригеревшее комманду, чтобы производить сверку
                        structure[key] = triggered_words
            else:
                # Если слова тригеры уже имеются - проводим проверку через них
                try:
                    #Если количество слов == максимальному количеству слов в структуре?
                    for key, value in structure.items():
                        if any(word.lower() in x for x in value):
                            continue
                        else:
                            del structure[key]
                except RuntimeError:
                    print('Уменьшены варианты искомых команд')

        if not structure:
            # не определенно ни одной комманды
            self.tts.say("Команда не ясна! Повторите пожалуйста!")
            return None
        elif len(structure.keys()) > 1:
            self.tts.say("Команда не ясна! Команда подходит сразу под %d условия" % len(structure.keys()))
            return None
        else:
            parse_data["command"] = self.commands[structure['key']]

        # получаем аргументы с их коммандами:
        # if parse_data['command']['args']:
        #    #TODO - какие слова являются аргументами, а какие данными???

        return parse_data

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
