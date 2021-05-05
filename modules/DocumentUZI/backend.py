"""Backend модуля DocumentUZI, отвечающий за создание, редактирование документов узи"""
import datetime
import os

from docxtpl import DocxTemplate
import shutil


# TODO КАК ОПРЕДЕЛИТЬ НАЗВАНИЯ ТИПОВ ИСЛЛЕДОВАНИЯ

class ResearchSession():
    ABS_PATH = os.path.abspath('./modules/DocumentUZI').replace('\\', '/')
    SRC_PATH = ABS_PATH + '/doc_src'
    OUTPUT_PATH = ABS_PATH + '/output_documents'
    FORMAT = '.docx'

    def __init__(self, name_patient: str, type_on_search: str):
        self.name_patient = name_patient  # имя пациента
        # TODO НАПИСАТЬ ОПРЕДЕЛИТЬ ТИПА ИССЛЕДОВАНИЯ
        self.type_research = type_on_search  # вид исследования
        self.name_docx = self.name_patient.replace(' ', '_') \
                         + datetime.date.today().strftime("%d_%m_%Y") + self.FORMAT

        self.docx_obj = self.create_document()
        self.context = {x: None for x in self.docx_obj.undeclared_template_variables}

    def get_type_research(self,type_on_search):
        #TODO ПОКА ЗАХОРДКОДЮ
        type_on_search

    def create_document(self) -> DocxTemplate:
        """Создание рабочего документа"""
        src_path = self.SRC_PATH + '/' + self.type_research  # TODO Заменить ???
        dst_path = self.OUTPUT_PATH + '/' + self.name_docx
        shutil.copyfile(src=src_path, dst=dst_path)
        return DocxTemplate(dst_path)

    def save_session(self):
        """Сохранение сессии"""
        self.docx_obj.render(self.context)
        self.docx_obj.save(self.OUTPUT_PATH + '/' + self.name_docx)

    def close_session(self):
        """Закрытие сессии"""
        self.save_session()

    def open_preview(self):
        """Открыть предварительный результат в word (Может и pdf сделать?)"""
        self.save_session()
        os.startfile(self.OUTPUT_PATH + '/' + self.name_docx)

    def send_document_to_print(self):
        self.save_session()
        os.startfile(self.OUTPUT_PATH + '/' + self.name_docx, 'print')

    def change_context(self, name, data):
        self.context[name] = data

