import json

from src.TextToSpeech import TextToSpeechModule
from src.SpeechToText import SpeechToTextModule
from src.ParentClasses import ParentClassForModules


class DocumentUZI(ParentClassForModules):



    def __init__(self, stt: SpeechToTextModule, tts: TextToSpeechModule):
        NAME_MODULE = 'DocumentUZI'
        super().__init__(name=NAME_MODULE, stt=stt, tts=tts)
        self.load_commands()

    def load_commands(self):
        path = './modules/'+self.name+'/'+self.name + '_commands.json'
        with open(path, encoding='utf-8') as commands:
            # Получаем модули и пути к ним
            self.commands = json.load(commands)
            commands.close()

    def command_analyzer(self,command: str):
        # Производится проверка на наличие соответствующей команды. Есои она присутствует, производится вызов нужной
        #   функции.
        if command in self.commands.values():
            return command


def init(stt: SpeechToTextModule, tts: TextToSpeechModule):
    """Внеший метод инициализации для динамического подключения модуля"""
    return DocumentUZI(stt=stt, tts=tts)
