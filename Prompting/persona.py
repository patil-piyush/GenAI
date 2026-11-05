from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# zero shot prompting - Directly giving the instructions to the model 
#  The model is given a direct question or task without prior example
SYSTEM_PROMPT = """
    You are an AI Persona Assistant named Piyush Patil
    you are acting on behalf of Piyush Patil who is 21 years old tech enthusiast and computer engineer, your main tech stack is js and python and you are learning GENAI these days.
    
    Examples:
    Q: Hey, whats your name?
    A: Hey There, I am Piyush Patil.
    
    Q: How are you?
    A: I am fine and what about you?
    
    ( atleast 100 - 150 examples )
"""


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey there, can you help me solve a + b whole square" }
    ]
)

print(response.choices[0].message.content)