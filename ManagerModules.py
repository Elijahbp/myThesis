import json

from TextToSpeech import TextToSpeechModule


class ManagerModules:
    # Менеджер модулей
    # Отвечает за инициализацию модулей. Для этого определяется файлы
    def __init__(self, tts: TextToSpeechModule):
        self.tts = tts

    def search_modules(self):
        json
