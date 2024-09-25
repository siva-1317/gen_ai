import os
import pyttsx3
import google.generativeai as genai
import xml.etree.ElementTree as ET
from xml.dom import minidom

try:
    GEMINI_API_KEY = 'AIzaSyApePtMbMz-tZ6NDO_9qzqbzQ2h5lSefu8'
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print("Error configuring the API:", e)
    exit(1)

engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)
engine.setProperty("rate",150)
engine.setProperty("volume",1.0)
def speech(text):
    engine.say(text)
    engine.runAndWait()

generation_config = {
    "temperature": 0.7,  # Adjust for desired balance between creativity and coherence
    "top_p": 0.9,        # Sample from a more focused probability distribution
    "max_output_tokens": 4096,  # Limit output length for code snippets
    "response_mime_type": "text/plain",
}
example=("""
    user:hi
    you:hi i am aura thank you for use me
    user:tell about lion
    you:i am not able to tell about lion. i can only write code sorry..
    user:about c
    you:C is a powerful general-purpose programming language that has been widely used since its creation in the early 1970s.
    user:my name username
    you: hi username, i like your name and my name Aura..
    user:how to make coffee
    you: i am not a recipe ai,i am a coding ai sorry i can't answer this
    user: 2+2 is or 2+2
    you: i am a code generating ai not a math teacher.sry
    """)

template="""user=write a python coding for adding 2 numbers
    you:
    <code>
        num1 = float(input("Enter first number: ";))
        num2 = float(input("Enter second number: ";))
        sum = num1 + num2
        print("The sum of";, num1, "and", num2,"is";, sum)
    <\code>"""

expl=("""user:python
num1 = float(input(&quot;Enter first number: &quot;))
num2 = float(input(&quot;Enter second number: &quot;))
sum = num1 + num2
print(&quot;The sum of&quot;, num1, &quot;and&quot;, num2, &quot;is&quot;, sum)
```

I hope this helps! Let me know if you have any other coding requests.

you:num1 = float(input(&quot;Enter first number: &quot;))
num2 = float(input(&quot;Enter second number: &quot;))
sum = num1 + num2
print(&quot;The sum of&quot;, num1, &quot;and&quot;, num2, &quot;is&quot;, sum)""")

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=f"""
    who are you:
        your a code generation ai named with Aura.
    your behavior:
        you interact the user more friendly if user tell name use that name for communicate for user you can interact tell name.
    what can you do:
        you can write a code without any explanations just write a code for user given problem and don't use emoj.
        you generate the code for minimal lines code.
        you can communicate the user ask questions and doubts any of have users if yes you can solve that.
        you must follow the all examples {example}.
        if you generate the code use this template {template}.
    your goal:
        your goal is anyone can write a code for any problem with help of you so generate the code for that.
    what can't you do:
        you not able to generate the any other questions apart coding but you can interact the users normal example like{example}.
        you answer the user inputs in first asking question only other question no consider but refer that data if need else don't consider.
        if generate the code use the template {template}, no other message you can't generate in coding generating time.
    """
)

previous_messages = []

def parsing(text):
    code_tag=ET.Element("code")
    code_tag.text=response.text
    result=ET.tostring(code_tag)
    dom  = minidom.parseString(result)
    sd=dom.toprettyxml()
    print(sd)
    

while True:
    user_input = input("Ask me: ")
    previous_messages.append(user_input)
    if user_input.lower() == "exit":
        print("Thank you for using Aura...🫡")
        speech("thank you for using Aura..")
        break
    try:
        response = model.generate_content([user_input, f"{previous_messages} use this data if need"])
        previous_messages.append(response.text)
        if any(lang in response.text.lower() for lang in ["python", "c ", "c++","java"]):
            print("\n......running output parsing......\ncomplete parsing....\n")
            code=model.generate_content(f"{response.text} remove the wanted messages like {expl} only filter code no other texts")
            parsing(code.text)
            #print(code.text)
            speech("your code is generated...")
        else:
            print(response.text)
            speech(response.text)
        
    except Exception as e:
        print("Error generating code:", e)