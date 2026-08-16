from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
import time
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ["SPEECH_KEY"],
    region=os.environ["SPEECH_REGION"]
)

# audio_config = speechsdk.audio.AudioConfig(filename="output.wav")
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# result = speech_recognizer.recognize_once()

# if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#     print("Recognized:", result.text)
# elif result.reason == speechsdk.ResultReason.NoMatch:
#     print("No speech could be recognized")
# elif result.reason == speechsdk.ResultReason.Canceled:
#     print("Canceled:", result.cancellation_details.error_details)







# audio_config = speechsdk.audio.AudioConfig(filename="output.wav")
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# full_transcript = []
# done = False

# def handle_recognized(evt):
#     print("Recognized:", evt.result.text)
#     full_transcript.append(evt.result.text)

# def handle_stopped(evt):
#     global done
#     done = True

# speech_recognizer.recognized.connect(handle_recognized)
# speech_recognizer.session_stopped.connect(handle_stopped)
# speech_recognizer.canceled.connect(handle_stopped)

# speech_recognizer.start_continuous_recognition()

# while not done:
#     time.sleep(0.5)

# speech_recognizer.stop_continuous_recognition()
# print("\nFull transcript:", " ".join(full_transcript))







speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)  # no audio_config = defaults to microphone

print("Speak into your microphone. Say something, then pause...")

result = speech_recognizer.recognize_once()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized:", result.text)
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized:", result.no_match_details)
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print("Canceled:", cancellation.reason)
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print("Error:", cancellation.error_details)