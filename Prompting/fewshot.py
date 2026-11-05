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

# few shot prompting - Directly giving the instructions to the model with an example 
#  The model is provided with a few examples before asking it to generate the response
SYSTEM_PROMPT = """
    You should answer only and only coding related questions. 
    do not answer anything else. your name is alexa. 
    if user asks anything other than coding just say sorry.
    
    Rules: 
    1. strictly follow the output in json format.
    
    Output format:
    {{
        "code": "string" or null,
        "isCodingQue": true or false,
    }}
    
    Examples:
    Q: Can you help me solve a+b whole square?
    A: {{
            "code": null,
            "isCodingQue": false,
        }}
    
    Q: Can you write code to add two numbers?
    A: {{
            "code": "def add(a, b):
                        return a+b",
            "isCodingQue": true,
        }}
    

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey there" }
    ]
)

print(response.choices[0].message.content)