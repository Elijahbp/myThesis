
from src.SpeechToText import SpeechToTextModule
from src.TextToSpeech import TextToSpeechModule

from abc import ABCMeta, abstractmethod
import json

from src.lib.MethodsForWords import get_count_word


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
        parse_data = self.get_structure_input_data(input_data=input_data)
        if not parse_data:
            return False
        else:
            return self.run_command(parse_data)

    @abstractmethod
    def run_command(self, parsed_data: dict):
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
        #   "data":
        # }
        # "2":{
        #   "name_arg": ,
        #   "data":
        # }
        # }
        parsed_data = {
            "command": None,
            "sets": {}
        }
        # парсим входную строку
        input_data = input_data.split(' ')
        count_word_input_data = len(input_data)
        # проверяем на комманды
        structure = {}
        count_word = 0
        max_count_word_command = 0
        for word in input_data:
            count_word += 1
            if count_word == 1:
                for key, value in self.commands.items():
                    # получаем перечень слов, которые были затригерены, и могут быть частью вводимой комманды
                    triggered_words = list(filter(lambda x: word.lower() in x, value['trigger_words']))
                    if triggered_words:
                        # получаем словосочетание, затригеревшее комманду, чтобы производить сверку
                        min_count_word_command = get_count_word(triggered_words,'min')
                        max_count_word_command = get_count_word(triggered_words,'max')
                        # если число слов >= числу в слов в команде, тогда берем её
                        if min_count_word_command <= count_word_input_data:
                            structure[key] = triggered_words
                if len(structure.keys()) == 1:
                    break
            elif structure:
                # Если слова тригеры уже имеются - проводим проверку через них
                    if count_word <= max_count_word_command:
                        try:
                            for key, value in structure.items():
                                if any(word.lower() in x for x in value):
                                    continue
                                elif count_word <= self.get_count_word(structure[key],'max'):
                                    # Удаляем только ту структуру, у которой слов в комманде >= count_word
                                    structure[key] = None
                                else:
                                    continue
                            structure = {x: y for x, y in structure.items() if y is not None}
                        except RuntimeError:
                            print('Уменьшены варианты искомых команд')
            else:
                return  None
        if not structure:
            # не определенно ни одной комманды
            #self.tts.say("Команда не ясна! Повторите пожалуйста!")
            return None
        elif len(structure.keys()) > 1:
            self.tts.say("Команда не ясна! Команда подходит сразу под %d условия" % len(structure.keys()))
            return None
        else:
            key = list(structure.keys())[0]
            parsed_data["command"] = self.commands[key]

        #получаем аргументы с их коммандами:
        #Проверяем аргументы у команды! Если в команде они не предусмотрены - отсекаем их!!!

        if parsed_data['command']['args']:
            i = 0
            for name_arg, type_arg in parsed_data['command']['args'].items():
                #проходимся по каждому следущему слову
                parsed_data['sets'][str(i)] = {}
                parsed_data['sets'][str(i)]['name_arg'] = name_arg
                if type(type_arg) is dict :
                    #Если тип данных raw - сырой, то тогда берем все данные, что идут после команды
                    parsed_data['sets'][str(i)]['data'] = input_data[count_word:]
                else:
                    parsed_data['sets'][str(i)]['data'] = input_data[count_word]

        return parsed_data




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
