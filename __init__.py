from SpeechToText import SpeechToTextModule
from TextToSpeech import TextToSpeechModule

# def test_microphone():
#     mic = sr.Microphone()
#     recog = sr.Recognizer()
#     while True:
#         with mic as audio_file:
#             print('Speech to microphone')
#             audio = recog.listen(source=audio_file,phrase_time_limit=10)
#             print("Converting Speech to Text...")
#             text_from_speech = recog.recognize_sphinx(audio_data=audio, language='ru-RU')
#             text_from_speech = recog.recognize_houndify(audio_data=audio,
#                                                                   client_id='wDZNQouAcQolOXkEx7K_6A==',
#                                                                   client_key='VHBYNcRARVn4zZtFi0jOKp3AqB3wqMRPu7u34sfu5dZRaAMJl53fPHHFhp-z2kkN9uPrATQNQBA2d1K4WntTug==')
#
#             print("You said: " + text_from_speech)
#             if text_from_speech == "выйти":
#                 print('Exit from speech-to-text program')


if __name__ == '__main__':
#    stt = SpeechToTextModule(recognizer_method='houndify')
    tts = TextToSpeechModule()
    while True:
        k = input()
        if k != "exit":
            tts.say(k)
        else:
            tts.say("Good Bye")
            break
    print('Good Bye')