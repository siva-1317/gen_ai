import os
import json
import google.generativeai as genai
from serpapi import GoogleSearch

GEMINI_API_KEY='AIzaSyCk-L3QFn35P646LN8IBkpwTKeneOoPrtA'

SERPAPI_API_KEY='fbde52eba9537013efedd82f945895665345f10045c0e685fe7760c40006eae0'

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,  # Adjust for desired balance between creativity and coherence
    "top_p": 0.9,        # Sample from a more focused probability distribution
    "max_output_tokens": 4096,  # Limit output length for code snippets
    "response_mime_type": "text/plain",
}


def get_answer_box(query):
    print("parsed query: ", query)

    search = GoogleSearch({
        "q": query, 
        "api_key": SERPAPI_API_KEY
    })
    result = search.get_dict()
    
    if 'answer_box' not in result:
        return "No answer box found"
    
    return result['answer_box']

get_answer_box_declaration = {
    'name': "get_answer_box",
    'description': "Get the answer box result for real-time data from a search query",
    'parameters': {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to search for"
            }
        },
        "required": [
            "query"
        ]
    },
}

prompt = input("enter the place of you want to know temperature : ")

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config= generation_config,
    )
response = model.generate_content(
    f"what is the temperature of {prompt} in now in celsius",
    tools=[{
        'function_declarations': [get_answer_box_declaration],
    }],
)

function_call = response.candidates[0].content.parts[0].function_call
args = function_call.args
function_name = function_call.name

if function_name == 'get_answer_box':
    result = get_answer_box(args['query'])

data_from_api = json.dumps(result)[:500]

response = model.generate_content(
    """
    Based on this information: `""" + data_from_api + """` 
    and this question: `""" + prompt + """`
    respond to the user in a friendly manner.
    """,
)
print(response.text)

