import os
import sys
import argparse
import json
from dotenv import load_dotenv
from groq import Groq
from functions.get_files_info import schema_get_files_info, get_files_info

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# System prompt with function usage instructions
system_prompt = """
You are a helpful AI coding agent.

You can perform the following operations:

- List files and directories using the get_files_info function

Only use the get_files_info function when the user specifically asks about files or directories. For other questions like math, greetings, or general queries, respond normally without calling any functions.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Create available functions list
available_functions = [schema_get_files_info]

# Get current working directory for function calls
working_directory = os.getcwd()

# Set up argument parser
parser = argparse.ArgumentParser(description='Generate content using Groq API')
parser.add_argument('prompt', help='The prompt to send to the AI model')
parser.add_argument('--verbose', action='store_true', help='Show detailed output including prompt and token counts')

# Parse arguments
args = parser.parse_args()
user_prompt = args.prompt
verbose = args.verbose

# Create messages list (Groq-adapted structure)
messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user", 
        "content": user_prompt
    }
]

# Update call to use the messages list with tools
response = client.chat.completions.create(
    model="llama3-8b-8192",  # Groq's 8B model with function calling support           
    messages=messages,
    tools=available_functions,
    tool_choice="auto"
)

# Output based on verbose flag
if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

# Check if the LLM called a function
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

if tool_calls:
    # LLM called a function, handle it
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        print(f"Calling function: {function_name}({function_args})")
        
        # Execute the function
        if function_name == "get_files_info":
            directory = function_args.get("directory", ".")
            result = get_files_info(working_directory, directory)
            print(f"Function result: {result}")
else:
    # No function call, just print the text response
    print(response_message.content)