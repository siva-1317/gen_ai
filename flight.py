import os
import google.generativeai as aura
from serpapi import GoogleSearch

api='AIzaSyApePtMbMz-tZ6NDO_9qzqbzQ2h5lSefu8'
aura.configure(api_key=api) 

generation_config = {
    "temperature": 0.9,  # Adjust for desired balance between creativity and coherence
    "top_p": 0.9,        # Sample from a more focused probability distribution
    "max_output_tokens": 4096,  # Limit output length for code snippets
    "response_mime_type": "text/plain",
}


model = aura.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""
    you can generate the three letter code for airport:
    example:
    input:what 3 letter code for chennai airport
    output:MAA
    
    "Provide flight details based on departure and/or arrival date and time as given by the user. Ensure to extract specific times from the query and use them to search for user given data. Return flight details in a structured format including airline, flight number, departure time, arrival time, duration, and price."

    Detailed Instructions:
    1. Extract Input: 
        Identify and extract the departure date and arrival date from the user's query.
        If either date is missing, assume flexibility and retrieve flights close to the provided time.
        Example:
        Input: "Show me flights departing 2024-09-17."
        Output: { "departure_date": "2024-09-17", "arrival_time": "any" }

    2. Access Database:
        Search the available flights using the user given data.
        Filter the flights based on the user-specified time window.

    3. Generate Response:
        Format the flight information in a clear and concise structure.
        Sample response:
            "Here are the flights departing at 9 AM:
            Airline: Delta, Flight Number: DL1523, Departure: 9:00 AM, Arrival: 12:15 PM, Price: $320, Duration: 3h 15m.
            Airline: United, Flight Number: UA245, Departure: 9:05 AM, Arrival: 12:20 PM, Price: $290, Duration: 3h 15m."

    4. Alternative Suggestions:
        If no exact matches are found, suggest alternate flights:
        "There are no flights exactly at 9 AM, but here are some options:
            Airline: Air India, Flight Number: AI345, Departure: 8:45 AM, Arrival: 12:00 PM."

    5. Personalization and Confirmation:
        Ask the user if they would like to book any of the suggested flights or explore more options.
            Example: "Would you like to book one of these flights, or should I search for different options?"

    """)

def air_code(place):
    code = model.generate_content(f"what 3 letter code for {place} airport only give a code only")
    return code.text
    
dep_place =input("enter the departure airport : ")
arr_place =input("enter the arrival airport : ")

sd=air_code(dep_place)
ds = air_code(arr_place)
print(sd)
print(ds)

fdate = input("enter the date of departure (yyyy/mm/dd) : ")
tdate = input("enter the date of arrival (yyyy/mm/dd) : ")


params = {
"engine": "google_flights",
"departure_id":sd,
"arrival_id":ds,
"outbound_date": fdate,
"return_date": tdate,
"currency": "INR",
"hl": "en",
"api_key": "fbde52eba9537013efedd82f945895665345f10045c0e685fe7760c40006eae0"
}

search = GoogleSearch(params)
results = search.get_dict()


try:
    user = f"{dep_place} to {arr_place} flight details"
    response = model.generate_content(f"answer this question {user} and use this dates {fdate} to {tdate} and use this data for answer the question {results} and answer the user for friendly")
    print(response.text)
except Exception as d:
    print("generating error : ",d)