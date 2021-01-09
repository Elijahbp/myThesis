import json

from src.TextToSpeech import TextToSpeechModule
from src.SpeechToText import SpeechToTextModule
from src.ParentClasses import ParentClassForModules


class DocumentUZI(ParentClassForModules):

    def __init__(self, stt: SpeechToTextModule, tts: TextToSpeechModule):
        name_module = 'DocumentUZI'
        super().__init__(name=name_module, stt=stt, tts=tts)
        self.info_str['name_ru'] = "Документы УЗИ"
        self.info_str['version'] = "0.1"
        self.load_commands()

    def load_commands(self):
        path = './modules/'+self.name+'/'+self.name + '_commands.json'
        with open(path, encoding='utf-8') as commands:
            # Получаем модули и пути к ним
            self.commands = json.load(commands)
            commands.close()


    def run_command(self, structure: dict, args: list):
        #TODO - провести разбор выполняемых команд
        return True

    def start(self):
        #TODO - реализовать

        return True

    def stop(self):
        #TODO - реализовать
        """Остановка модуля DocumentUZI"""
        return True


def init(stt: SpeechToTextModule, tts: TextToSpeechModule):
    """Внеший метод инициализации для динамического подключения модуля"""
    return DocumentUZI(stt=stt, tts=tts)
