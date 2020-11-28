from datetime import datetime

from SpeechToText import SpeechToTextModule
from TextToSpeech import TextToSpeechModule

from ManagerModules import ManagerModules
import json

STOP_ASSISTANT = 1

class Core:
    def __init__(self):
        self.stt = SpeechToTextModule(recognizer_method='houndify')
        self.tts = TextToSpeechModule()
        self.manager_modules = ManagerModules(tts=self.tts)
        self.main_commands = {}
        self.manager_modules_commands = {}
        with open('./src/main_commands.json', encoding='utf-8') as main_commands:
            loaded_json = json.load(main_commands)
            self.main_commands = loaded_json['сommands_main']
            self.manager_modules_commands = loaded_json['сommands_module_manager']

    def run(self):
        # Запуск
        self.tts.say('Инициализация произведена')
        # TODO: Сделать проверку на загружаемые модули
        work = True
        while True:
            #input_text = self.stt.get_textfromspeesh()
            input_text = input()
            result = self.command_analyzer(input_text)
            if result == STOP_ASSISTANT:
                return None

    def command_analyzer(self, input_command: str):
        # Todo: Подумать, может сделать общий пул комманд для увеличения скорости работы? Для этого будет
        #  производится поиск из всех комманд, и комманды будут содержать спец атрибут, отсылающий к типам команды:
        #  main/manager/module и сразу же будет происходить перенаправление xD
        for id,words in self.main_commands.items():
            if input_command in words:
                return self.run_main_command(int(id))
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
            str_time = f"{time.hour} часа {time.minute} минут"
            self.tts.say(str_time)
        elif id_command == 3:
            # Вывод дня/месяца/года
            date = datetime.now()
            str_date = f"Сегодня {date.day} {datetime.strftime(date, '%B')} {date.year} года"
            self.tts.say(str_date)
        return None
