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

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": "You are an expert in mathematics and only and only answer maths questions. If the query is not related to maths then just say sorry and do not answer that." },
        { "role": "user", "content": "Hey there, can you give me a python program that can print hello world" }
    ]
)

print(response.choices[0].message.content)