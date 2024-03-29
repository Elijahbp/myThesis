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
        self.commands = None
        self.dictionary_of_arguments = None
        self.load_commands()
        self.load_dictionary_of_arguments()
        self.research_session = None  # сессия исследования

    def load_commands(self):
        path = './modules/' + self.name + '/' + self.name + '_commands.json'
        with open(path, encoding='utf-8') as commands:
            # Получаем модули и пути к ним
            self.commands = json.load(commands)
            commands.close()

    def load_dictionary_of_arguments(self):
        path = './modules/' + self.name + '/doc_src/dictionary_of_protocols.json'
        with open(path, encoding='utf-8') as dictionary_of_protocols_json:
            # Получаем модули и пути к ним
            self.dictionary_of_arguments = json.load(dictionary_of_protocols_json)
            dictionary_of_protocols_json.close()

    def run_command(self, parsed_data: dict):
        # TODO - провести разбор выполняемых команд
        id = int(parsed_data['command']['id'])
        if id == 1:
            """Начать исследование"""
            self.start_research()
            self.tts.say("Исследование началось")
        elif id == 2:
            """Закончить исследование"""
            self.end_research()
        elif id == 3:
            """Заполнить/Изменить параметр"""
            self.set_parameter(parsed_data)
        elif id == 4:
            """Что осталось заполнить?"""
            self.what_is_left()
        elif id == 5:
            """Сохранить исследование"""
            self.save_research()
        elif id == 6:
            """Вывести результат"""
            self.get_preview_version()
        elif id == 7:
            """Печать документа"""
            self.print_research()
        elif id == 8:
            """Справка"""
            self.get_help_info()

        return True

    def start(self):
        # TODO - реализовать

        return True

    def stop(self):
        """Остановка модуля DocumentUZI"""
        # 1) Остановка сессии
        # 2) Очистка загруженных протоколов исследованния
        self.end_research()
        self.commands = None
        self.dictionary_of_arguments = None
        return True

    def start_research(self):
        # 1) Имя Клиента
        # 2) Тип исследования
        if not self.research_session:
            self.tts.say('Назовите имя пациента')
            name_patient = self.stt.get_text_from_speeсh()
            self.tts.say('Какое исследование вы хотите начать?')
            type_research = self.get_type_research()
            self.research_session = ResearchSession(name_patient=name_patient, type_research=type_research)
        else:
            self.tts.say("Предыдущая сессия не закончена. Завершить?")
            input_text = self.stt.get_text_from_speeсh().lower()
            if input_text == 'да':
                self.end_research()

    def end_research(self):
        """Завершение исследования"""
        if self.research_session:
            if self.research_session.close_session():
                self.tts.say("Сессия сохранена, и завершена!")
                self.research_session = None
            else:
                self.tts.say("Не все данные заполнены! Желаете закончить сессию?")
                while True:
                    input_text = self.stt.get_text_from_speeсh().lower()
                    if input_text == 'да':
                        self.research_session.close_session(force_exit=True)
                        self.tts.say('Сессия завершена')
                        self.research_session = None
                        return True
                    elif input_text == 'нет':
                        return False
                    else:
                        self.tts.say('Команда не ясна. Пожалуйста повторите!')
        else:
            self.tts.say("Отсутствует рабочая сессия!")
            return False

    def set_parameter(self, parsed_data:dict):
        """Заполнить/Изменить параметр"""
        if self.research_session:
            result = self.research_session.change_context(parsed_data['sets']['0'])
            if result[0]:
                self.tts.say(result[1] + '- заполнено')
            else:
                self.tts.say(result[1])
        else:
            self.tts.say('Сессия не запущена!')

    def what_is_left(self):
        """Что осталось?"""
        if self.research_session:
            str_on_say = self.research_session.get_info_whats_left()
            self.tts.say(str_on_say)
        else:
            self.tts.say('Сессия не запущена! Для получения информации - начните сессию')

    def get_preview_version(self):
        """Вывести результат"""
        if self.research_session:
            self.research_session.open_preview()
        else:
            self.tts.say('Сессия не запущена! Для получения предварительной версии документа - начните сессию')

    def save_research(self):
        """Сохранение результата """
        if self.research_session:
            self.research_session.save_session()
            self.tts.say("Результат сохранён!")
        else:
            self.tts.say('Сессия не запущена! Для сохранения сессии, сначала её нужно начать!')

    def print_research(self):
        """Печать документа"""
        if self.research_session:
            self.research_session.send_document_on_print()
            self.tts.say("Документ напечатан!")
        else:
            self.tts.say('Печать невозможна, так как нет открытой сессии!')

    def get_type_research(self):
        """Определение типа искомого исследования"""
        # Проходимся по всему словарю протоколов
        type_research = None
        while type_research is None:
            type_on_search = self.stt.get_text_from_speeсh().lower()
            for id, type_research_structure in self.dictionary_of_arguments.items():
                if type_on_search in type_research_structure["trigger_words"]:
                    return type_research_structure

    def get_help_info(self):
        self.tts.say(
            """
            Для работы с модулем Исследование узи необходимо использовать голосовые команды:
            Начать исследование; Сохранить исследование; Закончить исследование;
            Заполнить или изменить - необходимо для записи данных исследования;
            Что осталось - перечисление параметров, которые не были заполнены;
            Вывести результат - открывается файл исследования в office word;
            Печать - отправляет файл исследования на печать;
            """
        )





def init(stt: SpeechToTextModule, tts: TextToSpeechModule):
    """Внеший метод инициализации для динамического подключения модуля"""
    return DocumentUZI(stt=stt, tts=tts)
