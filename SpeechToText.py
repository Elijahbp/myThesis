import speech_recognition as sr

class SpeechToTextModule():
    def __init__(self, index_microphone = 1, recognizer_method ='sphinx', language ='ru-RU'):
        self.index_microphone = index_microphone
        self.language = language
        self.recognizer = sr.Recognizer()
        self.recognizer_method = recognizer_method

    def get_textfromspeesh(self):
        audio = self.listen()
        text_from_speech = self.start_recognize(audio=audio)
        return text_from_speech

    def listen(self):
        mic = sr.Microphone(device_index=self.index_microphone)
        with mic as audio_file:
            print('Speech to microphone')
            audio = self.recognizer.listen(source=audio_file,phrase_time_limit=10)
            return audio

    def start_recognize(self,audio):
        print("Converting Speech to Text...")
        text_from_speech = ''
        if self.recognizer_method == 'sphinx':
            text_from_speech = self.recognizer.recognize_sphinx(audio_data=audio, language=self.language)
        elif self.recognizer_method == 'google':  # необходима настройка
            text_from_speech = self.recognizer.recognize_google(audio_data=audio,key = None,language='ru-RU')
        elif self.recognizer_method == 'houndify':  # необходима настройка
            text_from_speech = self.recognizer.recognize_houndify(audio_data=audio,client_id='wDZNQouAcQolOXkEx7K_6A==',client_key='VHBYNcRARVn4zZtFi0jOKp3AqB3wqMRPu7u34sfu5dZRaAMJl53fPHHFhp-z2kkN9uPrATQNQBA2d1K4WntTug==')
        print("You said: " + text_from_speech)
        return text_from_speech