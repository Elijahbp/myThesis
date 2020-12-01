import pkgutil
import json

from TextToSpeech import TextToSpeechModule
from SpeechToText import SpeechToTextModule

class ManagerModules:
    # Менеджер модулей
    # Отвечает за инициализацию модулей. Для этого определяется файлы
    def __init__(self, stt: SpeechToTextModule, tts: TextToSpeechModule):
        self.stt = stt
        self.tts = tts
        self.manager_modules_commands = {}
        self.modules = {}
        self.search_modules()


    def search_modules(self):
        with open('./src/modules_list.json', encoding='utf-8') as modules_json:
            #Получаем модули и пути к ним
            modules_path = json.load(modules_json)
            for name,path in modules_path['modules'].items():
                #Инициируем модули
                #self.modules[name] = __import__(name=)

                self.tts.say('Модуль '+name+ ' - инизиализирован!')

            modules_json.close()



    def command_analyzer(self, input_command: str):
        #1) Проверка на команду менеджера
        #2) Проверка на команду запущенных модуля (потом реализовать модулей?)
        #
        return
