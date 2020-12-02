import json

from src.TextToSpeech import TextToSpeechModule
from src.SpeechToText import SpeechToTextModule
from src.ParentClasses import ParentClassForModules


class DocumentUZI(ParentClassForModules):

    def __init__(self, name: str, stt: SpeechToTextModule, tts: TextToSpeechModule):
        super().__init__(name=name,stt=stt, tts=tts)
        self.load_commands()

    def load_commands(self):
        path = './modules/'+self.name+'/'+self.name + '_commands.json'
        with open(path, encoding='utf-8') as commands:
            # Получаем модули и пути к ним
            self.commands = json.load(commands)
            commands.close()


def init(name: str, stt: SpeechToTextModule, tts: TextToSpeechModule):
    return DocumentUZI(name=name, stt=stt, tts=tts)
