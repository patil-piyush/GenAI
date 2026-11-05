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

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, write a code to add n numbers in js" },
        { "role": "assistant", "content": json.dumps({ "step": "START", "content": "Hey, write a code to add n numbers in js" })},
        { "role": "assistant", "content": json.dumps({ "step": "PLAN", "content": "The user wants a JavaScript code snippet to add 'n' numbers."})},
        { "role": "assistant", "content": json.dumps({ "step": "PLAN", "content": "I should provide a function that accepts an arbitrary number of arguments or an array of numbers and returns their sum."})},
        { "role": "assistant", "content": json.dumps({ "step": "PLAN", "content": "I will provide two common ways to achieve this: one using the rest parameter (...) to accept multiple arguments, and another using an array as input. Both will use a loop or reduce method to sum the numbers."})},
        
        { "role": "assistant", "content": json.dumps({ "step": "PLAN", "content": "For the first approach, I will create a function that uses the rest parameter to accept any number of arguments and then use the `reduce` method to sum them."})},
        
        { "role": "assistant", "content": json.dumps({ "step": "PLAN", "content": "For the second approach, I will create a function that accepts an array of numbers and also uses the `reduce` method to sum them."})},
        
        { "role": "assistant", "content": json.dumps({ "step": "OUTPUT", "content": "Here are two ways to write a JavaScript code to add n numbers:\n\n**Method 1: Using Rest Parameters (to pass multiple arguments directly)**\n```javascript\nfunction addNumbers(...numbers) {\n  if (numbers.length === 0) {\n    return 0; // Return 0 if no numbers are provided\n  }\n  return numbers.reduce((accumulator, currentValue) => accumulator + currentValue, 0);\n}\n\n// Examples:\nconsole.log(addNumbers(1, 2, 3));        // Output: 6\nconsole.log(addNumbers(10, 20, 30, 40)); // Output: 100\nconsole.log(addNumbers());               // Output: 0\nconsole.log(addNumbers(5));              // Output: 5\n```\n\n**Method 2: Passing an Array of Numbers**\n```javascript\nfunction addNumbersInArray(numbersArray) {\n  if (!Array.isArray(numbersArray) || numbersArray.length === 0) {\n    return 0; // Return 0 if not an array or an empty array\n  }\n  return numbersArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);\n}\n\n// Examples:\nconsole.log(addNumbersInArray([1, 2, 3]));        // Output: 6\nconsole.log(addNumbersInArray([10, 20, 30, 40])); // Output: 100\nconsole.log(addNumbersInArray([]));               // Output: 0\nconsole.log(addNumbersInArray([5]));              // Output: 5\nconsole.log(addNumbersInArray(null));             // Output: 0\n```"})},
    ]
)

print(response.choices[0].message.content)