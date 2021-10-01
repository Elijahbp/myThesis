"""Backend модуля DocumentUZI, отвечающий за создание, редактирование документов узи"""
import datetime
import json
import os
import platform
import subprocess
import time

from docxtpl import DocxTemplate
import shutil

from src.lib.MethodsForWords import get_count_word


class ResearchSession():
    ABS_PATH = os.path.abspath('./modules/DocumentUZI').replace('\\', '/')
    SRC_PATH = ABS_PATH + '/doc_src'
    OUTPUT_PATH = ABS_PATH + '/output_documents'
    FORMAT = '.docx'

    def __init__(self, name_patient: str, type_research: dict):
        # 1) Получаем имя пациента
        # 2) Получаеи тип исследования
        # 3) Создаем копию протокола с новым именем
        # 4) Загружаем в переменную словарь контекста
        self.name_patient = name_patient  # имя пациента
        self.type_research = type_research  # вид исследования
        self.research_date = datetime.date.today().strftime("%d_%m_%Y")
        self.name_docx = self.name_patient.replace(' ', '_') + '_' \
                         + type_research['name_protocol'].replace(' ', '_') \
                         + '_' + self.research_date + self.FORMAT
        self.docx_obj = self.create_document()
        self.dictionary_context = self.get_dictionary_context()
        self.context = {x: '' for x in self.docx_obj.undeclared_template_variables}
        self.context['name_patient'] = self.name_patient
        self.context['research_date'] = self.research_date

    def get_dictionary_context(self) -> dict:
        """Получение словаря контекста протокола"""
        src_path = self.SRC_PATH + '/' + self.type_research['name_protocol'] + '/dictionary_of_context.json'
        with open(src_path, encoding='utf-8') as dictionary_context_json:
            # Получаем модули и пути к ним
            dictionary_context = json.load(dictionary_context_json)
            dictionary_context_json.close()
        if self.check_context(dictionary_context):
            return dictionary_context
        else:
            return None  # TODO ПЕРЕСМОТРЕТЬ, МОЖЕТ СДЕЛАТЬ CALLBACK

    def check_context(self,dictionary_context) -> bool:
        """Проверка контекста"""
        # TODO ДОДЕЛАТЬ!!!!
        if self.docx_obj.undeclared_template_variables == dictionary_context.keys():
            return True
        else:
            return False

    def create_document(self) -> DocxTemplate:
        """Создание рабочего документа, и выгрузка """
        src_path = self.SRC_PATH + '/' + self.type_research['name_protocol'] + '/' + self.type_research[
            'filename_protocol']
        dst_path = self.OUTPUT_PATH + '/' + self.name_docx
        shutil.copyfile(src=src_path, dst=dst_path)
        return DocxTemplate(dst_path)

    def save_session(self):
        """Сохранение сессии"""
        # ТЕГИ ОБЯЗАТЕЛЬНО СОХРАНЯТЬ!!!
        # дозаполнять пустые теги в контексте, после - очищать из них
        but_context = self.context
        for x, y in but_context.items():
            if not y:
                but_context[x] = '{{' + x + '}}'
        self.docx_obj.render(but_context)
        self.docx_obj.save(self.OUTPUT_PATH + '/' + self.name_docx)

    def close_session(self, force_exit=False):
        """Закрытие сессии"""
        # 1) Проверка на заполненные данные
        # 2) Если сохранение нужно в любом случае -
        if not force_exit:
            for x, y in self.context.items():
                if y == '':
                    return False
        self.docx_obj.render(self.context)
        self.docx_obj.save(self.OUTPUT_PATH + '/' + self.name_docx)
        return True

    def open_preview(self):
        """Открыть предварительный результат в word (Может и pdf сделать?)"""
        # СОздаем копию основного файла, заполняем контекстом, именуем с ~$, запускаем файл, после закрытия - удаляем
        src_path = self.OUTPUT_PATH + '/' + self.name_docx
        dst_path = self.OUTPUT_PATH + '/~$' + self.name_docx
        shutil.copyfile(src=src_path, dst=dst_path)
        copy_doc = DocxTemplate(dst_path)
        copy_doc.render(context=self.context)
        copy_doc.save(dst_path)
        if platform.system() == 'Windows':
            os.startfile(dst_path)
        elif platform.system() == 'Darwin':
            subprocess.call(['open', dst_path])
        time.sleep(5)  # Ожидание, пока программа запускается
        while True:
            try:
                os.remove(dst_path)
                break
            except IOError:
                """Ожидание закрытие ворда"""

    def send_document_on_print(self):
        """Отправка документа на печать"""
        src_path = self.OUTPUT_PATH + '/' + self.name_docx
        dst_path = self.OUTPUT_PATH + '/~$' + self.name_docx
        shutil.copyfile(src=src_path, dst=dst_path)
        copy_doc = DocxTemplate(dst_path)
        copy_doc.render(context=self.context)
        copy_doc.save(dst_path)
        os.startfile(dst_path, 'print')
        time.sleep(8)
        os.remove(dst_path)

    def get_info_whats_left(self):
        output_str = ''
        for x, y in self.context.items():
            if y == '':
                output_str += self.dictionary_context[x]['text_on_speech'] + '\n'
                continue
        if output_str == '':
            output_str = 'Все данные заполнены!'
        else:
            output_str = 'Осталось заполнить:\n' + output_str
        return output_str

    def change_context(self, parsed_data: dict):
        result = self.get_data_from_raw(parsed_data)
        if result[0]:
            self.context[result[0]] = result[1]
            return (True, self.dictionary_context[result[0]]["text_on_speech"])
        else:
            return result

    def get_data_from_raw(self, parsed_data: dict):
        name_context = None
        data = None
        # парсим входную строку
        count_word_input_data = len(parsed_data['data'])
        # проверяем на комманды
        structure = {}
        count_word = 0
        max_count_word_command = 0
        for word in parsed_data['data']:
            count_word += 1
            if count_word == 1:
                for key, value in self.dictionary_context.items():
                    # получаем перечень слов, которые были затригерены, и могут быть частью вводимой комманды
                    triggered_words = list(filter(lambda x: word.lower() in x, value['trigger_words']))
                    if triggered_words:
                        # получаем словосочетание, затригеревшее комманду, чтобы производить сверку
                        min_count_word_command = get_count_word(triggered_words, 'min')
                        max_count_word_command = get_count_word(triggered_words, 'max')
                        # если число слов >= числу в слов в команде, тогда берем её
                        if min_count_word_command <= count_word_input_data:
                            structure[key] = triggered_words
                if len(structure.keys()) == 1:
                     break
            elif structure:
                # Если слова тригеры уже имеются - проводим проверку через них
                    if count_word <= max_count_word_command:
                        try:
                            for key, value in structure.items():
                                if any(word.lower() in x for x in value):
                                    continue
                                elif count_word <= get_count_word(structure[key],'max'):
                                    # Удаляем только ту структуру, у которой слов в комманде >= count_word
                                    structure[key] = None
                                else:
                                    continue
                            structure = {x: y for x, y in structure.items() if y is not None}
                        except RuntimeError:
                            print('Уменьшены варианты искомых команд')
            else:
                break
        if not structure:
            return (False,"Имя контекста нераспознано. Пожалуйста, повторте ещё раз!")
        elif len(structure.keys()) > 1:
            return (False,"Имя контекста нераспознано не ясно! Имя подходит сразу к нескольким контекстам")
        else:
            name = list(structure.keys())[0]
            raw_data = (' ').join(parsed_data['data'][count_word:])
            return (name, raw_data)