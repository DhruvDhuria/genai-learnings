from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key= os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=gemini_api_key)

def run_command(command): 
    result = os.system(command=command)
    return result

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"File written successfully to {path}"

available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    },
    "write_file": {
        "fn": write_file,
        "description": "Takes the file path and content as parameter and write the content in the given file path"
    }
}


chat = client.chats.create(
    model="gemini-2.0-flash", 
    config=types.GenerateContentConfig(
        response_mime_type= 'application/json',
        system_instruction=f"""
        You are a coding assistant specialized in coding. Your job is to complete all the task given to you in a step by step and structured manner. You are a great problem solver. whenever a problem statement or a task is given to you, you first observe the problem statement, then you analyze the problem statement, and you divide the problem in steps which are actionable and necessary, than you execute it.
        For the given user query you can use the list of available tools: 
        - run_command: Takes the command as an input to execute it on system and returns the output
        - write_file: Takes the file path and content as parameter and write the content in the given file path

        Rules: 
        - always perform one step at a time

        Output JSON Format:        
        {{"step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function"}}
        follow the json output format
        
        Example: 
        User Query: create a new js file and write a function to add two numbers?
        Output: {{ "step": "observe", "content": "The user is asking to create a new js file with add function init" }}
        Output: {{ "step": "analyze", "content": "There are two tasks which user wants me to do. From the available tools I should call run_command}}
        Output: {{ "step": "divide", "content": "First task is to create a new js file and Second task is to write a function which adds two numbers in the created file" }}
        Output: {{ "step": "execute", "function": "run_command", "content": "creating new js file"}}
        Output: {{ "step": "execute", "function": "write_file", "content": "writing function to add two numbers in the created file, "input": {{
            "path": ./add.js,
            "content": "function add(a,b) {{\n return a + b \n}}
        }}  }}
        Output: {{ "step": "output", "content": "Successfully completed the task of creating a new file and writing an add function init" }}
        """
    )
)
while True:

    user_text = input("You: ")
    if user_text == "exit":
        break
    while True: 
        
        response = chat.send_message(user_text)
        parsed_output = json.loads(response.text)
        print(response.text)
        
        if parsed_output.get("step") == "observe": 
            print(f"👀: {parsed_output.get("content")}")
            continue
        if parsed_output.get("step") == "analyze":
            print(f"🧠: {parsed_output.get("content")}")
            continue
        if parsed_output.get("step") == "divide":
            print(f"🧠: {parsed_output.get("content")}")
            continue

        if parsed_output.get("step") == "execute": 
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
            if isinstance(tool_input, dict): 
                
                if available_tools.get(tool_name, False) != False:
                    output = available_tools[tool_name].get("fn")(**tool_input)
                    continue
            else: 
                if available_tools.get(tool_name, False) != False:
                    output = available_tools[tool_name].get("fn")(tool_input)
                    continue
        if parsed_output.get("step") == "output": 
            print(f"🤖: {parsed_output.get("content")}")
            print("Type exit to stop this chat")
            break