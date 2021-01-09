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
        super(ManagerModules, self).__init__(name=name_manager, stt=stt, tts=tts)
        self.info_str['name_ru'] = "Менеджер модулей"
        self.info_str['version'] = "0.1"
        self.load_commands()
        self.modules = {}  # Содержит структуру {'NameModule':{'class':fromimportlib',
        # 'module':obj,
        # 'status':STATUS_WORK}}
        self.search_modules()
        # Изначально запущен только менеджер модулей, но далее, при запуске новых данное поле будет обновляться
        self.pool_all_commands_modules = {
            self: ','.join(self.commands.keys()),
        }


    def load_commands(self):
        """Загрузка команд ядра и менеджера"""
        with open('resources/main_commands.json', encoding='utf-8') as main_commands:
            loaded_json = json.load(main_commands)
            self.commands = loaded_json['сommands_module_manager']
            main_commands.close()

    def search_modules(self):
        """Поиск модулей на подключение"""
        with open('resources/modules_list.json', encoding='utf-8') as modules_json:
            # Получаем модули и пути к ним
            modules_path = json.load(modules_json)
            for name, path in modules_path['modules'].items():
                # Инициируем модули
                self.modules[name] = {
                    'class': getattr(importlib.import_module(name=name), name),
                    'module': None,
                    'status': STATUS_WORK['ready']
                }
                self.tts.say('Модуль ' + name + ' - добавлен в пул!')
            modules_json.close()


    def run_command(self, structure: dict, args: list):
        id = int(structure['id'])
        "Поолучение аргументов в соответсвии со структурой"
        parameters = self.get_parameters_with_name(structure=structure, args=args)
        if not parameters:
            return False
        if id == 1:
            # Запуск модуля с определенным имененем
            self.start_module(parameters['name_module'])
        if id == 2:
            # Остановка модуля по имени
            self.stop_module(parameters['name_module'])
        if id == 3:
            # Вывести список модулей
            self.get_info_modules(parameters['status_module'])
        if id == 4:
            # Получить информацию менеджере модулей
            self.info()

    def start_module(self, name_module):
        self.tts.say('Запуск модуля ' + name_module)
        class_module = self.modules[name_module]['class']
        module_obj = self.modules[name_module]['module'] = class_module(stt=self.stt, tts=self.tts)
        result = module_obj.start()
        if result:
            self.modules[name_module]['status'] = STATUS_WORK['started']
            self.pool_all_commands_modules[module_obj] = ','.join(module_obj.commands.keys())
            self.tts.say('Модуль ' + name_module + ' - запущен!')
            return True
        else:
            self.tts.say('При запуске модуля ' + name_module + ' произошла ошибка!')
            return False

    def stop_module(self, name_module):
        self.tts.say('Остановка модуля ' + name_module)
        result = self.modules[name_module]['module'].stop()
        if result:
            self.tts.say('Выполнено')
            #TODO - Очищать ли из памяти объект модуля?
            self.modules[name_module]['status'] = STATUS_WORK['stopped']
            del self.pool_all_commands_modules[self.modules[name_module]['module']]
            return True
        else:
            return False

    def get_info_modules(self, status_module):
        output_info = 'Список запущенных модулей: \n'
        for name, value in self.modules.items():
            output_info += value['module'].info() + '\n'
        self.tts.say(output_info)
        return True
