from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def run_command(cmd: str):
    result = os.system(cmd)
    return result

# Tool/function to get weather details of any city
def get_weather_info( city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    
    response = requests.get(url)
    
    if(response.status_code == 200):
        return f"Weather in {city.lower()}: {response.text}"

    return "Something went wrong while fetching the weather information. Please try again later."


available_tools = {
    "get_weather_info": get_weather_info,
    "run_command": run_command
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
    { "step": "START/PLAN/OUTPUT/TOOL", "content": "string", "tool": "string", "input": "string" }
    
    
    Available Tools:
    1. get_weather_info(city: str) : This tool can be used to get the weather information of any city. It takes a city name as input and returns the weather information of that city.
    2. run_command(cmd: str) : This tool can be used to run a shell command. It takes a command as input and returns the exit code of the command.


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


print("\n")


class myOutputFormat(BaseModel):
    step: str = Field(..., description="The step of the process: START, PLAN, OUTPUT, TOOL")
    content: Optional[str] = Field(None, description="The Optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to be called")
    input: Optional[str] = Field(None, description="The input params for the tool to be called")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_query = input("👦 ->> ")
    message_history.append({ "role": "user", "content": user_query})


    while True:
        # response = client.chat.completions.parsed(
        #     model="gemini-2.5-flash",
        #     response_format=myOutputFormat,
        #     messages= message_history
        # )
        
        from openai import BadRequestError

        try:
            response = client.chat.completions.parse(
                model="gemini-2.5-flash",
                messages=message_history,
                response_format={"type": "json_object"}
            )
        except BadRequestError as e:
            print("API ERROR:", e)
            print("ERROR DETAILS:", e.response.text)
            raise
        
        # raw_result = response.choices[0].message.parsed
        # message_history.append({"role": "assistant", "content": raw_result})
        
        raw_result = response.choices[0].message.content

        parsed_result = myOutputFormat.model_validate_json(raw_result)

        message_history.append({
            "role": "assistant",
            "content": raw_result
        })
        
        # parsed_result = response.choices[0].message.parsed
        
        if parsed_result.step == "START":
            print("starting LLM", parsed_result.content)
            continue
        
        if parsed_result.step == "TOOL":
            print("Calling Tool", parsed_result.tool, "with input", parsed_result.input)
            tool_name = parsed_result.tool
            tool_input = parsed_result.input
            
            tool_response = available_tools[tool_name](tool_input)
            message_history.append({"role": "developer", "content": json.dumps(
                { "step": "OBSERVE", "tool": tool_name, "input": tool_input,"output": tool_response }
            )})
            continue
        
        if parsed_result.step == "PLAN":
            print("Planning", parsed_result.content)
            continue
        
        if parsed_result.step == "OUTPUT":
            print("\n🤖 ->> ", parsed_result.content)
            break



print("\n\n\n\n")

