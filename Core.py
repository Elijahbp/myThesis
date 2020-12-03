from datetime import datetime

from src.SpeechToText import SpeechToTextModule
from src.TextToSpeech import TextToSpeechModule
from ManagerModules import ManagerModules
from src.lib.StringDateAndTime import *

import json

STOP_ASSISTANT = 1


class Core:
    #TODO - добавит ли свои исключения в работе?
    def __init__(self):
        self.stt = SpeechToTextModule(recognizer_method='houndify')
        self.tts = TextToSpeechModule()
        self.commands = {}
        self.manager_modules = ManagerModules(stt=self.stt, tts=self.tts)
        self.load_commands()
        self.tts.say('Инициализация произведена')

    def load_commands(self):
        """Загрузка команд ядра и менеджера"""
        with open('resources/main_commands.json', encoding='utf-8') as main_commands:
            loaded_json = json.load(main_commands)
            self.commands = loaded_json['сommands_main']
            self.manager_modules.commands = loaded_json[
                'сommands_module_manager']  # Присваивание команд менеджеру
            main_commands.close()

    def run(self):
        """Запуск штатного режима голосового ассистента"""
        run = True
        while run:
            # input_text = self.stt.get_textfromspeesh()
            input_text = input()
            result = self.command_analyzer(input_text)
            if result == STOP_ASSISTANT:
                run = False
                continue
        self.tts.say("Lol kek chebureck")

    def command_analyzer(self, input_command: str):
        # Todo: Подумать, может сделать общий пул комманд для увеличения скорости работы? Для этого будет
        #  производится поиск из всех комманд, и комманды будут содержать спец атрибут, отсылающий к типам команды:
        #  main/manager/module и сразу же будет происходить перенаправление xD

        for id, words in self.commands.items():
            if input_command in words:
                return self.run_main_command(int(id))
        #Если команда обращена не к ядру, передаем её на исполнение в менеджере
        self.manager_modules.command_analyzer(input_command)
        return

    def run_main_command(self, id_command: int):
        #TODO - расширить функциональность
        """Обработчик команд ядра"""
        # При изменении списка команд - обязательно редактировать и эту функцию!!!
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
