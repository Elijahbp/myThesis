import speech_recognition as sr
import urllib.request
import json

from pyaudio import PyAudio


#if __name__ == '__main__':
#    FOLDER_ID = "b1g4qtn86ad59aqsjtco"  # Идентификатор каталога
#    IAM_TOKEN = "t1.9euelZrNlomKzIqQkI-VkJGNzJ2Vku3rnpWak8nPmMuKnMqUy57MnpKMkJvl8_cTfBB7-e9LWihb_N3z91MqDnv570taKFv8.jWaojHafqmqLX1lkO9F0eXUQ01Q3tz3bkUagSSNGSRjccpMaKkrnXSmSfkURfRtpAUfaUSe3MeFp4a0o6E9iAQ"  # IAM-токен
#
#    mic = sr.Microphone(device_index=0)
#    with mic as audio_file:
#        print('Speech to microphone')
#        audio = PyAudio.
#        sr.Recognizer.
#
#    data = audio
#    #with open("speech.ogg", "rb") as f:
#    #    data = f.read()
#
#    params = "&".join([
#        "topic=general",
#        "folderId=%s" % FOLDER_ID,
#        "lang=ru-RU"
#    ])
#
#    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
#    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)
#
#    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
#    decodedData = json.loads(responseData)
#
#    if decodedData.get("error_code") is None:
#        print(decodedData.get("result"))


class SpeechToTextModule:
    def __init__(self, index_microphone=1, recognizer_method='yandex', language='ru-RU'):
        self.index_microphone = index_microphone
        self.language = language
        self.recognizer = sr.Recognizer()
        self.recognizer_method = recognizer_method
        if self.recognizer_method == 'yandex':
            self.FOLDER_ID = ""
            self.IAM_TOKEN = ""
            self.params = "&".join([
                "topic=general",
                "folderId=%s" % self.FOLDER_ID,
                "lang=ru-RU"
            ])

    def get_text_from_speeсh(self):
        """Получение транскрибации текста (внешняя функция для вызова)"""
        text_from_speech = input()
        #audio = self.listen()
        #text_from_speech = self.start_recognize(audio=audio)
        return text_from_speech

    def listen(self):
        """Прослушивание микрофона"""
        mic = sr.Microphone(device_index=self.index_microphone)
        with mic as audio_file:
            print('Speech to microphone')
            audio = self.recognizer.listen(source=audio_file, phrase_time_limit=10)
            return audio

    def start_recognize(self, audio):
        """Функция транскрибации голоса (перевода речи в текст)"""
        print("Converting Speech to Text...")
        text_from_speech = ''
        if self.recognizer_method == 'sphinx':
            text_from_speech = self.recognizer.recognize_sphinx(audio_data=audio, language=self.language)
        elif self.recognizer_method == 'google':  # необходима настройка
            text_from_speech = self.recognizer.recognize_google(audio_data=audio, key=None, language='ru-RU')
        elif self.recognizer_method == 'houndify':  # необходима настройка
            text_from_speech = self.recognizer.recognize_houndify(audio_data=audio,
                                                                  client_id='wDZNQouAcQolOXkEx7K_6A==',
                                                                  client_key='VHBYNcRARVn4zZtFi0jOKp3AqB3wqMRPu7u34sfu5dZRaAMJl53fPHHFhp-z2kkN9uPrATQNQBA2d1K4WntTug==')
        elif self.recognizer_method == 'yandex':
            #with open("speech.ogg", "rb") as f:
            #    data = f.read()
            data = audio
            url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % self.params,
                                         data=data)
            url.add_header("Authorization", "Bearer %s" % self.IAM_TOKEN)
            responseData = urllib.request.urlopen(url).read().decode('UTF-8')
            decodedData = json.loads(responseData)

            if decodedData.get("error_code") is None:
                print(decodedData.get("result"))

            text_from_speech = decodedData.get("result")

        print("You said: " + text_from_speech)
        return text_from_speech
