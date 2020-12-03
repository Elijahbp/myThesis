import importlib
import json

from src.TextToSpeech import TextToSpeechModule
from src.SpeechToText import SpeechToTextModule
from src.ParentClasses import ParentClassForModules

STATUS_WORK = {
        'ready': 1,
        'started': 2,
        'stopped': 3,
        'closed': 4
}
class ManagerModules(ParentClassForModules):
    # Менеджер модулей
    # Отвечает за инициализацию модулей. Для этого определяется файлы



    def __init__(self, stt: SpeechToTextModule, tts: TextToSpeechModule):
        name_manager = 'ManagerModules'
        super(ManagerModules, self).__init__(name=name_manager,stt= stt,tts= tts)
        self.modules = {} # Содержит структуру {'NameModule':{'class':obj_fromimportlib','module':obj,'status':''}}
        self.search_modules()

    def search_modules(self):
        """Поиск модулей на подключение"""
        with open('resources/modules_list.json', encoding='utf-8') as modules_json:
            # Получаем модули и пути к ним
            modules_path = json.load(modules_json)
            for name, path in modules_path['modules'].items():
                # Инициируем модули
                self.modules[name] = {
                    'class': importlib.import_module(name=name),
                    'module': None,
                    'status': STATUS_WORK['ready']
                }
                self.tts.say('Модуль ' + name + ' - добавлен в пул!')

            modules_json.close()

    def command_analyzer(self, input_command: str):
        # 1) Проверка на команду менеджера
        # 2) Проверка на команду запущенных модуля (потом реализовать в модуле???)
        for id,words in self.commands.values():
            if input_command in words:
                self.run_manager_command(id=int(id))

        return

    def run_manager_command(self, id: int,**kwargs):
        if id == 1:
            # Запуск модуля с определенным имененем
            self.start_module(kwargs['name_module'])
        if id == 2:
            # Остановка модуля по имени
            self

    def start_module(self,name_module):
        self.tts = 'Запуск модуля ' + name_module
        class_module = self.modules[name_module]['class']
        self.modules[name_module]['module'] = class_module.init( stt=self.stt, tts=self.tts)
        self.modules[name_module]['status'] = STATUS_WORK['started']
        self.tts = 'Модуль ' + name_module + ' - запущен!'
        return True

    def stop_module(self, name_module):
        self.tts = 'Остановка модуля ' + name_module
        self.modules[name_module]['module'].stop()