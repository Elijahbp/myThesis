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
        self.modules = {}
        # Содержит структуру
        # {
        # 'NameModule':{'class':fromimportlib',
        # 'module':obj,
        # 'status':STATUS_WORK
        # }}
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
            modules = json.load(modules_json)
            for name, structure in modules['modules'].items():
                # Инициируем модули
                self.modules[name] = {
                    'class': getattr(importlib.import_module(name=name), name),
                    'module': None,
                    'status': STATUS_WORK['ready'],
                    'text_on_speech':
                        structure['text_on_speech'],
                    "trigger_name":
                        structure['trigger_name']
                }
                self.tts.say('Модуль ' + self.modules[name]['text_on_speech'] + ' - добавлен в пул!')
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
        elif id == 2:
            # Остановка модуля по имени
            # TODO: сделать проверку имени
            self.stop_module(parameters['name_module'])
        elif id == 3:
            # Вывести список модулей
            self.get_info_modules(parameters['status_module'])
        elif id == 4:
            # Получить информацию менеджере модулей
            self.info()

    def start_module(self, trigger_word):
        """Запуск модуля по его имени"""
        name_module = self.check_name(trigger_word)
        if name_module:
            if self.modules[name_module]['status'] != STATUS_WORK['started']:
                self.tts.say('Запуск модуля ' + self.modules[name_module]['text_on_speech'])
                class_module = self.modules[name_module]['class']  # Получаем класс модуля
                module_obj = self.modules[name_module]['module'] = class_module(stt=self.stt,
                                                                                tts=self.tts)  # Инициализируем объект класса
                result = module_obj.start()  # Запускаем модуль
                if result:
                    # В рамках менеджера - переводим статус работы модуля в "Started", добавляем комманды модуля в пул всех
                    # команд
                    self.modules[name_module]['status'] = STATUS_WORK['started']
                    self.pool_all_commands_modules[module_obj] = ','.join(module_obj.commands.keys())
                    self.tts.say('Модуль ' + self.modules[name_module]['text_on_speech'] + ' - запущен!')
                    return True
                else:
                    self.tts.say(
                        'При запуске модуля ' + self.modules[name_module]['text_on_speech'] + ' произошла ошибка!')
                    return False
            else:
                self.tts.say('Модуль ' + self.modules[name_module]['text_on_speech'] + " уже запущен")
                return False
        else:
            self.tts.say('Имя модуля не распознано! Пожалуйста, повторите команду.')

    def stop_module(self, trigger_word):
        name_module = self.check_name(trigger_word)
        if name_module:
            if self.modules[name_module]['status'] == STATUS_WORK['started']:
                self.tts.say('Остановка модуля ' + self.modules[name_module]['text_on_speech'])
                result = self.modules[name_module]['module'].stop()
                if result:
                    self.tts.say('Выполнено')
                    self.modules[name_module]['status'] = STATUS_WORK['stopped']
                    del self.pool_all_commands_modules[self.modules[name_module]['module']]
                    self.modules[name_module]['module'] = None
                    return True
                else:
                    return False
            else:
                self.tts.say('Модуль ' + self.modules[name_module]['text_on_speech'] + " не запущен")
                return False
        else:
            self.tts.say('Имя модуля не распознано! Пожалуйста, повторите комманду.')

    def check_name(self, trigger_word):
        """Проверка входящего имени комманды на корректность"""
        for name, structure in self.modules.items():
            if trigger_word in structure['trigger_name']:
                return name
        else:
            return False

    def get_info_modules(self, status_module):
        output_info = 'Список запущенных модулей: \n'
        for name, structure in self.modules.items():
            output_info += structure['module'].info() + '\n'
        self.tts.say(output_info)
        return True
