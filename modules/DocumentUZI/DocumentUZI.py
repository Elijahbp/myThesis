import json

from backend import ResearchSession
from src.TextToSpeech import TextToSpeechModule
from src.SpeechToText import SpeechToTextModule
from src.ParentClasses import ParentClassForModules


class DocumentUZI(ParentClassForModules):

    def __init__(self, stt: SpeechToTextModule, tts: TextToSpeechModule):
        name_module = 'DocumentUZI'
        super().__init__(name=name_module, stt=stt, tts=tts)
        self.info_str['name_ru'] = "Документы УЗИ"
        self.info_str['version'] = "0.1"
        self.load_commands()
        self.research_session : ResearchSession # сессия исследования


    def load_commands(self):
        path = './modules/' + self.name + '/' + self.name + '_commands.json'
        with open(path, encoding='utf-8') as commands:
            # Получаем модули и пути к ним
            self.commands = json.load(commands)
            commands.close()

    def run_command(self, structure: dict, args: list):
        # TODO - провести разбор выполняемых команд
        id = int(structure['id'])
        if id == 1:
            """Начать исследование"""
            self.start_research()
        elif id == 2:
            """Закончить исследование"""
            self.close_session()
        elif id == 3:
            """Заполнить параметр"""
        elif id == 4:
            """Изменить параметр"""
        elif id == 5:
            """Что осталось заполнить?"""
        elif id == 6:
            """Сохранить исследование"""
        elif id == 7:
            """Вывести результат"""
        elif id == 8:
            """Печать документа"""
        elif id == 9:
            """Справка"""

        return True

    def start(self):
        # TODO - реализовать

        return True

    def stop(self):
        # TODO - реализовать
        """Остановка модуля DocumentUZI"""
        return True

    def start_research(self):
        # 1) Имя Клиента
        # 2) Тип исследования
        self.tts.say('Назовите имя пациента')
        name_patient = self.stt.get_text_from_speeсh()
        self.tts.say('Какое исследование вы хотите начать?')
        type_research = self.stt.get_text_from_speeсh()
        self.research_session = ResearchSession(name_patient=name_patient, type_research=type_research)

    def end_research(self):
        """Завершение исследования"""
        self.research_session.close_session()
        self.tts.say('Завершение исследования!')


def init(stt: SpeechToTextModule, tts: TextToSpeechModule):
    """Внеший метод инициализации для динамического подключения модуля"""
    return DocumentUZI(stt=stt, tts=tts)
