import os
import google.generativeai as genai


try:
    GEMINI_API_KEY = 'AIzaSyApePtMbMz-tZ6NDO_9qzqbzQ2h5lSefu8'
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print("Error configuring the API:", e)
    exit(1)


generation_config = {
    "temperature": 0.7,  
    "top_p": 0.9,        
    "max_output_tokens": 4096, 
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

name=input("i am aura, and like to know your beautiful name you can tell me :")
print("hi ",name,",your name is nice !!!")
lang="english"
place=input("you can tell me which place you like to visit :")
place.lower()
sd=f" i like to go for visiting {place} so you guide me for which places are famous in tourism of this place.generate the output in {lang} language with proper letter placing"
try:
    response = model.generate_content([sd])                
    print(response.text)
    print("thank you for visiting aura trips")
except Exception as e:
    print("Error planning tour:", e)