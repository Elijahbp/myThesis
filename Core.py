from datetime import datetime

from src.SpeechToText import SpeechToTextModule
from src.TextToSpeech import TextToSpeechModule
from src.ParentClasses import ParentClassForModules
from ManagerModules import ManagerModules
from src.lib.StringDateAndTime import *

import json

STOP_ASSISTANT = 1


class Core(ParentClassForModules):
    #TODO - добавить ли свои исключения в работе?
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
            self.commands = loaded_json['сommands_main']
            main_commands.close()

    def run(self):
        """Запуск штатного режима голосового ассистента"""
        run = True
        while run:
            # input_text = self.stt.get_textfromspeesh()
            input_text = input()
            result = self.localisation_command(input_text)
            if result is STOP_ASSISTANT:
                run = False
                continue

    def localisation_command(self, input_command: str):
        """Метод определяет, к какому куда необходимо перенаправить команду"""
        # for commands, module_obj in self.pool_all_commands:
        #    if input_command
        if self.analyze_command_and_run(input_command=input_command):
            return True
            # Если команда обращена не к ядру, передаем её на исполнение в менеджере
        else:
            # ПРобиваем на наличие введенной комманды из всего пула комманд всех модулей по очереди
            try:
                for module, words in self.manager_modules.pool_all_commands_modules.items():
                    # Если часть находится в каком-то модуле - передаем все данные в этот модуль на анализ
                    if module.analyze_command_and_run(input_command):
                        return True
                    else:
                        continue
            except RuntimeError:
                print('Из-за добавления модуля, размер списка комманд модуля был увеличен.'
                      ' Исключительный случай был обработан')

        return

    def run_command(self, structure: dict, args: list):
        """Обработчик команд ядра"""
        # При изменении списка команд - обязательно редактировать и эту функцию!!!
        id_command = int(structure['id'])
        if id_command == 1:
            # Выключение ассистента
            self.tts.say('Выключение ассистента.')
            return STOP_ASSISTANT
        elif id_command == 2:
            # Вывод времени минуты/секунды
            time = datetime.now()
            str_time = f"{get_hour_str(time.hour)} {get_minute_str(time.minute)}"
            self.tts.say(str_time)
        elif id_command == 3:
            # Вывод дня/месяца/года
            date = datetime.now()
            str_date = f"Сегодня {date.day} {get_month_gen(date.month)} {date.year} года"
            self.tts.say(str_date)
        return None
