from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
import time
import azure.cognitiveservices.speech as speechsdk

translation_config = speechsdk.translation.SpeechTranslationConfig(
    subscription=os.environ["SPEECH_KEY"],
    region=os.environ["SPEECH_REGION"]
)
translation_config.speech_recognition_language = "en-US"
translation_config.add_target_language("hi")  # Hindi
translation_config.add_target_language("fr")  # French

audio_config = speechsdk.audio.AudioConfig(filename="output.wav")
recognizer = speechsdk.translation.TranslationRecognizer(
    translation_config=translation_config,
    audio_config=audio_config
)

import time
done = False
results = []

def handle_recognized(evt):
    print(f"Original: {evt.result.text}")
    for lang, translation in evt.result.translations.items():
        print(f"  -> {lang}: {translation}")

def handle_stopped(evt):
    global done
    done = True

recognizer.recognized.connect(handle_recognized)
recognizer.session_stopped.connect(handle_stopped)
recognizer.canceled.connect(handle_stopped)

recognizer.start_continuous_recognition()
while not done:
    time.sleep(0.5)
recognizer.stop_continuous_recognition()