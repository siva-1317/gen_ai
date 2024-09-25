import pyttsx3
import sys
import io
from googletrans import Translator
from gtts import gTTS
import os


engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)

#text to speech
def speech(text):
    engine.say(text)
    engine.runAndWait()
    
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Create a Translator object
translator = Translator()
promt=input("enter the prompt :")
# Translate English to Tamil
result = translator.translate(promt, src='en', dest='ta')
sd=result.text
# Print the translated text
print(sd)
speech(sd)