import speech_recognition as sr

def test_microfone():
    mic = sr.Microphone(device_index=1)
    recog = sr.Recognizer()
    with mic as audio_file:
        print('Speech to microphone')
        audio = recog.listen(source=audio_file,phrase_time_limit=10)

        print("Converting Speech to Text...")
        text_from_speech = recog.recognize_sphinx(audio_data=audio, language='ru-RU')
        print("You said: " + text_from_speech)
        if text_from_speech == "выйти":
            print('Exit from speech-to-text program')

if __name__ == '__main__':
    test_microfone()
