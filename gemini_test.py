import google.generativeai as genai
genai.configure(api_key="api key to be updated later")
model=genai.GenerativeModel("gemini-2.0-flash")
response=model.generate_content("Give me 2-day itinerary for a trip to Mysuru")
print(response.text)

try: 
    response=model.generate_content("Give me 2-day itinerary for a trip to Mysuru")
    print(response.text)
except Exception as e:
    print(e)



























