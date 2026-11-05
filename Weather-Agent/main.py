from openai import OpenAI
from dotenv import load_dotenv
import os 
import requests

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
) 



def get_eather_info( city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    
    response = requests.get(url)
    
    if(response.status_code == 200):
        return f"Weather in {city.lower()}: {response.text}"

    return "Something went wrong while fetching the weather information. Please try again later."



def main():
    print("\n")
    user_query = input("👦 ->> ")
    
    response =  client.chat.completions.create(
        model = "gemini-2.5-flash",
        messages = [
            { "role": "user", "content": user_query }
        ]
    )
    
    
    print(f"\n🤖 ->> {response.choices[0].message.content}\n\n\n")
    
    
    
# main()

print(get_eather_info("Sangli"))