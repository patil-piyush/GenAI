from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
    you are an expert AI assistant in resolving user queries using chain of thought.
    you work on START, PLAN and OUTPUT steps.
    you need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT. 
    
    
    Rules:
    - Strictly follow the given JSON output format
    - Only run one step at a time. 
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT ( which is going to the displayed to the user ).
    
    
    Output JSON Format:
    { "step": "START/PLAN/OUTPUT", "content": "string" }
    
    Example:
    START: Hey, can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS rule" } 
    PLAN: { "step": "PLAN", "content": "yes, the BODMAS rule applies here" }
    PLAN: { "step": "PLAN", "content": "first we must multiply 3 and 5 which is 15" }
    PLAN: { "step": "PLAN", "content": "now the new equation becomes 2 + 15 / 10" }
    PLAN: { "step": "PLAN", "content": "we must perform the division 15 / 10 which is 1.5" }
    PLAN: { "step": "PLAN", "content": "now the new equation becomes 2 + 1.5" }
    PLAN: { "step": "PLAN", "content": "now finally, we can add 2 and 1.5 which is 3.5" }
    PLAN: { "step": "PLAN", "content": "greate, we have solved the problem and finally left with 3.5 as answer" }
    OUTPUT: { "step": "OUTPUT", "content": "The answer is 3.5" }
"""


print("\n\n\n\n")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]


user_query = input("input --> ")
message_history.append({ "role": "user", "content": user_query})


while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages= message_history
    )
    
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    
    parsed_result = json.loads(raw_result)
    
    if parsed_result.get("step") == "START":
        print("starting LLM", parsed_result.get("content"))
        continue
    
    if parsed_result.get("step") == "PLAN":
        print("Planning", parsed_result.get("content"))
        continue
    
    if parsed_result.get("step") == "OUTPUT":
        print("RESULT", parsed_result.get("content"))
        break



print("\n\n\n\n")

