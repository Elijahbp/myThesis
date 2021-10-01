Структура команд

"name_command":{
    "id":"n",
    "trigger_words": ["cлово/сочетание"]
    "args":{
        "arg_name_1":{
            "type_data":"int/float/str/bool/raw",
            "count_input_data":"k"
        }
        "arg_name_2":{
            "parameter_name":"str",
            "type_data":"int/float/str/bool/raw",
            "count_input_data":"k"
        }
    }
}

"exit":{
      "id": "1",
      "args": {},
      "trigger_words": ["выход","exit"]
},

"name_tag": {
    "text_on_speech": "Текст, что будет говорить ассистент",
    "trigger_words": ["слово/сочетание"],
    "type_data": "int/float/str/bool/raw"
}

  "name_patient": {
    "text_on_speech": "Полное имя пациента",
    "trigger_words": ["имя пациента"],
    "type_data": "str"
  }



Пул всех команд:
    {
        "all_commands_module": Module_obj
    }


Типы данных: ["int","float","str","bool","raw"]

Статусы модуля:
    Запущенные
    Остановленные
    (all)

Типы протоколов - словарь:
    Узлы
    Кишечник
    Малтаз
    Молочные железы
