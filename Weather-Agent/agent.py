from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# Tool/function to get weather details of any city
def get_weather_info( city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    
    response = requests.get(url)
    
    if(response.status_code == 200):
        return f"Weather in {city.lower()}: {response.text}"

    return "Something went wrong while fetching the weather information. Please try again later."


available_tools = {
    "get_weather_info": get_weather_info
}

SYSTEM_PROMPT = """
    you are an expert AI assistant in resolving user queries using chain of thought.
    you work on START, PLAN and OUTPUT steps.
    you need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT. 
    You can also call a toll if you think it is necessary to call a tool to get the information from the list od available tools.
    for every tool call, wait for the observe step which is the output of the tool and then continue with your PLAN and finally give an OUTPUT. 
    
    Rules:
    - Strictly follow the given JSON output format
    - Only run one step at a time. 
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT ( which is going to the displayed to the user ).
    
    
    Output JSON Format:
    { "step": "START/PLAN/OUTPUT/TOOL", "content": "string", "Tool": "string", "Input": "string" }
    
    
    Available Tools:
    1. get_weather_info(city: str) -> str : This tool can be used to get the weather information of any city. It takes a city name as input and returns the weather information of that city.
        
    Example 1:
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
    
    
    Example 2:
    START: Hey, what is the weather in Sangli?
    PLAN: { "step": "PLAN", "content": "Seems like user is interested in weather information of Sangli in India" }
    PLAN: { "step": "PLAN", "content": "Lets see if any tool is available to get the weather information from list of available tools" } 
    PLAN: { "step": "PLAN", "content": "great we have get_weather_info tool available for this query" }
    PLAN: { "step": "PLAN", "content": "I need to call get_weather_info with Sangli as the argument" }
    PLAN: { "step": "TOOl", "tool": "get_weather_info", "input": "Sangli" }
    PLAN: { "step": "OBSERVE", "tool": "get_weather_info", "output": "The Temperature of Sangli is Cloudy 25°C" }
    PLAN: { "step": "PLAN", "content": "great, we have the weather information for Sangli" }
    OUTPUT: { "step": "OUTPUT", "content": "The current weather in Sangli is Cloudy with a temperature of 25°C." }
"""


print("\n\n\n\n")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]


user_query = input("👦 ->> ")
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
    
    if parsed_result.get("step") == "TOOL":
        print("Calling Tool", parsed_result.get("tool"), "with input", parsed_result.get("input"))
        tool_name = parsed_result.get("tool")
        tool_input = parsed_result.get("input")
        
        tool_response = available_tools[tool_name](tool_input)
        message_history.append({"role": "developer", "content": json.dumps(
            { "step": "OBSERVE", "tool": tool_name, "input": tool_input,"output": tool_response }
        )})
        continue
    
    if parsed_result.get("step") == "PLAN":
        print("Planning", parsed_result.get("content"))
        continue
    
    if parsed_result.get("step") == "OUTPUT":
        print("\n🤖 ->> ", parsed_result.get("content"))
        break



print("\n\n\n\n")

