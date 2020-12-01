from TextToSpeech import TextToSpeechModule
from SpeechToText import SpeechToTextModule

import json

class DocumentUZI:

    def __init__(self, stt: SpeechToTextModule, tts: TextToSpeechModule):
        self.stt = stt
        self.tts = tts
        self.commands = ()

    def load_commands(self):
        with open('DocumentUZI_commands.json', encoding='utf-8') as commands:
            #Получаем модули и пути к ним
            self.commands =json.load(commands)
            commands.close()
