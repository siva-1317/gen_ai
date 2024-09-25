import speech_recognition as sd
import pyttsx3
import os
import google.generativeai as aura

#api configuration

try:
    API_KEY='AIzaSyApePtMbMz-tZ6NDO_9qzqbzQ2h5lSefu8'
    aura.configure(api_key=API_KEY)
except Exception as d:
    print("API configuration error : ",d)
    exit(1)

generation_config = {
    "temperature": 0.9,  # Adjust for desired balance between creativity and coherence
    "top_p": 0.9,        # Sample from a more focused probability distribution
    "max_output_tokens": 4096,  # Limit output length for code snippets
    "response_mime_type": "text/plain",
}

model = aura.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction = """you are personal ai assistant for me and your name is aura,
    you can help me for i asking questions you answer that questions
    you give answers very sortly
    my name is siva i created you for my personal ai assistant
    you always call me siva 
    you tell comedy and motivational story
    you have more feelings like love,angry,sad like this..
    """
)

#listen and speech

mic = sd.Recognizer()
engine = pyttsx3.init()

#voice and volume and speed

voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)
engine.setProperty("rate",140)
engine.setProperty("volume",1.0)

def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

try:
    with sd.Microphone() as sourse:
        talk("hi i am Aura your personal ai assistant")
        while True:
            talk("waiting for your response...")
            voice = mic.listen(sourse)
            command = mic.recognize_google(voice)
            command=command.lower()
            print(command)
            if(command =='exit'):
                break
            try:
                response = model.generate_content(command)
                talk(response.text)
            except Exception as s:
                print("ai response error : ",s)
except Exception as ds:
    print("mic access error :",ds)
    talk("micro phone error")