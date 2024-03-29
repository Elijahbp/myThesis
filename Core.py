from datetime import datetime

from src.SpeechToText import SpeechToTextModule
from src.TextToSpeech import TextToSpeechModule
from src.ParentClasses import ParentClassForModules
from ManagerModules import ManagerModules
from src.lib.StringDateAndTime import *

import json

STOP_ASSISTANT = 1


class Core(ParentClassForModules):
    def __init__(self):
        name = "Core"
        stt = SpeechToTextModule(recognizer_method='houndify')
        tts = TextToSpeechModule()
        super(Core, self).__init__(name=name, stt=stt, tts=tts)
        self.manager_modules = ManagerModules(stt=self.stt, tts=self.tts)
        self.load_commands()
        self.tts.say('Инициализация произведена')


    def load_commands(self):
        """Загрузка команд ядра и менеджера"""
        with open('resources/main_commands.json', encoding='utf-8') as main_commands:
            loaded_json = json.load(main_commands)
            self.commands = loaded_json['сommands_core']
            main_commands.close()

    def run(self):
        """Запуск штатного режима голосового ассистента"""
        run = True
        result = None
        while run:
            input_data = self.stt.get_text_from_speeсh()
            if input_data == '':
                self.tts.say('Команда не распознана. Повторите пожалуйста!')
            else:
                result = self.localisation_command(input_data)
            if result is STOP_ASSISTANT:
                run = False
                continue

    def localisation_command(self, input_data: str):
        """Метод определяет, к какому модулю необходимо перенаправить команду"""
        res_core = self.analyze_command_and_run(input_data=input_data)
        if res_core:
            return res_core
            # Если команда обращена не к ядру, передаем её на исполнение в менеджер
        else:
            # Побиваем на наличие введенной команды из всего пула команд всех модулей по очереди
            try:
                res_modules = None
                for module, words in self.manager_modules.pool_all_commands_modules.items():
                    # Если часть находится в каком-то модуле - передаем все данные в этот модуль на анализ
                    if module.analyze_command_and_run(input_data):
                        return True
                    else:
                        continue
                if not res_modules:
                    self.tts.say('Команда не распознана. Повторите пожалуйста!')
            except RuntimeError:
                print('Из-за добавления модуля, размер списка команд модуля был увеличен.'
                      ' Исключительный случай был обработан')

    def run_command(self, parsed_data:dict):
        """Обработчик команд ядра"""
        # При изменении списка команд - обязательно редактировать и эту функцию!!!
        id_command = int(parsed_data['command']['id'])
        if id_command == 1:
            # Выключение ассистента
            self.tts.say('Выключение ассистента.')
            return STOP_ASSISTANT
        elif id_command == 2:
            # Вывод времени минуты/секунды
            time = datetime.now()
            str_time = f"{get_hour_str(time.hour)} {get_minute_str(time.minute)}"
            self.tts.say(str_time)
            return True
        elif id_command == 3:
            # Вывод дня/месяца/года
            date = datetime.now()
            str_date = f"Сегодня {date.day} {get_month_gen(date.month)} {date.year} года"
            self.tts.say(str_date)
            return True
        return False
