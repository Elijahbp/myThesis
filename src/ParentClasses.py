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


    def command_parser(self, input_command: str) -> list:
        # разбиваем строку на элементы
        input_words = input_command.split(' ')
        return input_words

    def analyze_command_and_run(self, input_command: str):
        command_data = []
        command_data = self.command_parser(input_command=input_command)
        key_word = command_data[0].lower()  # TODO: Страшная условность - необходимо переосмыслить!!!
        for key_words, structure in self.commands.items():
            if key_word in key_words:
                self.run_command(structure, command_data)
                return True
        else:
            return False

    @abstractmethod
    def run_command(self, structure: dict, args: list):
        pass

    def get_parameters_with_name(self, structure: dict, args: list):
        # правило для определения кол-ва параметров
        # 1) Все аргументы идут в самом конце
        parameters = {}
        # Если аргумент не один, тогда есть вероятность, что там есть передаваемый параметр
        if len(args) > 1:
            i = 0
            # TODO Сделать опциональные параметры!!!
            count_parameters = len(structure['args'].keys())
            if count_parameters > 0:
                for arg in args[len(args) - count_parameters:]:
                    # Порядок параметров должен быть в соответствии с порядком
                    key_meta_argument = list(structure['args'].keys())[i]
                    output_value = None
                    try:
                        if structure['args'][key_meta_argument] == 'str':
                            output_value = str(arg)
                        elif structure['args'][key_meta_argument] == 'int':
                            output_value = int(arg)
                        elif structure['args'][key_meta_argument] == 'float':
                            output_value = float(arg)
                        elif structure['args'][key_meta_argument] == 'bool':
                            output_value = bool(arg)
                        elif structure['args'][key_meta_argument] == 'var':
                            #TODO произвести идентификацию типа, если var!!!
                            print('ПРОИЗВЕСТИ ИДЕНТИФИКАЦИЮ ТИПА!!!!')
                    except:
                        self.tts.say("Параметр " + arg + '- явялется недопустимым!')
                        return False
                    parameters[key_meta_argument] = output_value
                    i += 1
        return parameters

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
