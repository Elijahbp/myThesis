from datetime import datetime

from SpeechToText import SpeechToTextModule
from TextToSpeech import TextToSpeechModule
import json

class Core():
    def __init__(self):
        self.stt = SpeechToTextModule(recognizer_method='houndify')
        self.tts = TextToSpeechModule()
        self.main_commands = {}
        self.manager_modules_commands = {}
        #with open('./src/main_commands.json',encoding='utf-8') as main_commands:
        #    loaded_json = json.load(main_commands)
        #    self.main_commands = loaded_json['сommands_main']
        #    self.manager_modules_commands = loaded_json['сommands_module_manager']

        print('ok')

    def run(self):
        # Запуск
        self.tts.say('Инициализация произведена')
        # TODO: Сделать проверку на загружаемые модули
        work = True
        while True:
            input_text = self.stt.get_textfromspeesh()
            result = self.command_analyzer(input_text)



    def command_analyzer(self, input_command:str):
        #Todo: Подумать, может сделать общий пул комманд для увеличения скорости работы?
        #   Для этого будет производится поиск из всех комманд, и комманды будут содержать
        #   спец атрибут, отсылающий к типам команды: main/manager/module и сразу же будет происходить перенаправление xD
        # Первое - должна возвращаться структура ['уровень команды',"id команды", "текст команды"]

        return


    def run_main_command(self,id_command:int):
        # При изменении списка команд - обязательно редактировать и эту функцию!!!
        if id_command == 1:
            #Выключение ассистента
            return "down assistant"
        elif id_command == 2:
            #Вывод времени минуты/секунды
            time = datetime.now()
            str_time = f"{time.hour} часов {time.minute} минут"
            self.tts.say(str_time)
        elif id_command == 3:
            #Вывод дня/месяца/года
            date = datetime.now()
            str_date = f"Сегодня {date.day} {datetime.strftime(date,'%B')} {date.year} года"
            self.tts.say(str_date)
        return None
