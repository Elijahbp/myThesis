from datetime import datetime

from src.SpeechToText import SpeechToTextModule
from src.TextToSpeech import TextToSpeechModule
from ManagerModules import ManagerModules
from src.lib.StringDateAndTime import *

import json

STOP_ASSISTANT = 1


class Core:
    def __init__(self):
        self.stt = SpeechToTextModule(recognizer_method='houndify')
        self.tts = TextToSpeechModule()
        self.main_commands = {}
        self.manager_modules = ManagerModules(stt=self.stt, tts=self.tts)
        self.load_commands()

    def load_commands(self):
        with open('resources/main_commands.json', encoding='utf-8') as main_commands:
            loaded_json = json.load(main_commands)
            self.main_commands = loaded_json['сommands_main']
            self.manager_modules.manager_modules_commands = loaded_json['сommands_module_manager']
            main_commands.close()

    def run(self):
        # Запуск
        self.tts.say('Инициализация произведена')
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

        # 1) Формируем пул из всех команд
        # 2)
        for id, words in self.main_commands.items():
            if input_command in words:
                return self.run_main_command(int(id))
        self.manager_modules.command_analyzer(input_command)
        return

    def run_main_command(self, id_command: int):
        # При изменении списка команд - обязательно редактировать и эту функцию!!!
        if id_command == 1:
            # Выключение ассистента
            self.tts.say('Выключение ассистента.')
            return STOP_ASSISTANT
        elif id_command == 2:
            # Вывод времени минуты/секунды
            time = datetime.now()
            #time = datetime(2020,6,3,2,22)
            str_time = f"{get_hour_str(time.hour)} {get_minute_str(time.minute)}"
            self.tts.say(str_time)
        elif id_command == 3:
            # Вывод дня/месяца/года
            date = datetime.now()
            str_date = f"Сегодня {date.day} {get_month_gen(date.month)} {date.year} года"
            self.tts.say(str_date)
        return None
