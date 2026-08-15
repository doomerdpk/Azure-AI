from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ["SPEECH_KEY"],
    region=os.environ["SPEECH_REGION"]
)
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

result = synthesizer.speak_text_async("Hello! This is my first text to speech call using Azure AI Speech Services.").get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized and saved to output.wav")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print("Speech synthesis canceled:", cancellation.reason)
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print("Error details:", cancellation.error_details)