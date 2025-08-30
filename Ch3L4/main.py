import os
import sys
import argparse
import json
from dotenv import load_dotenv
from groq import Groq
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


class GroqFunctionCall:
    """Simple class to mimic Gemini's types.FunctionCall structure for Groq."""
    def __init__(self, name, args):
        self.name = name
        self.args = args


class GroqContent:
    """Simple class to mimic Gemini's types.Content structure for Groq."""
    def __init__(self, role, parts):
        self.role = role
        self.parts = parts


class GroqPart:
    """Simple class to mimic Gemini's types.Part structure for Groq."""
    def __init__(self, function_response):
        self.function_response = function_response
    
    @classmethod
    def from_function_response(cls, name, response):
        function_response = type('FunctionResponse', (), {'response': response})()
        return cls(function_response)


def call_function(function_call_part, verbose=False):
    """
    Handle calling one of our four functions based on the function_call_part.
    
    Args:
        function_call_part: Object with .name (string) and .args (dict) properties
        verbose: If True, print detailed function call information
        
    Returns:
        GroqContent object with function response
    """
    function_name = function_call_part.name
    function_args = function_call_part.args.copy()  # Make a copy to avoid modifying original
    
    # Print function call information
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Add working_directory to args - set to ./calculator as specified
    function_args["working_directory"] = "./calculator"
    
    # Dictionary mapping function names to actual functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    
    # Check if function name is valid
    if function_name not in function_map:
        return GroqContent(
            role="tool",
            parts=[
                GroqPart.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Call the function with keyword arguments
    try:
        function_result = function_map[function_name](**function_args)
        return GroqContent(
            role="tool",
            parts=[
                GroqPart.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return GroqContent(
            role="tool",
            parts=[
                GroqPart.from_function_response(
                    name=function_name,
                    response={"error": f"Function execution failed: {str(e)}"},
                )
            ],
        )

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# System prompt with function usage instructions
system_prompt = """
You are a helpful AI coding agent.

You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Only use these functions when the user specifically asks for file operations. For other questions like math, greetings, or general queries, respond normally without calling any functions.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Create available functions list
available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

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
        
        # Create a GroqFunctionCall object and use our call_function
        function_call_part = GroqFunctionCall(function_name, function_args)
        function_call_result = call_function(function_call_part, verbose)
        
        # Check if we got a valid response
        if not hasattr(function_call_result, 'parts') or not function_call_result.parts:
            raise Exception("call_function did not return a valid response with parts")
        
        if not hasattr(function_call_result.parts[0], 'function_response') or not hasattr(function_call_result.parts[0].function_response, 'response'):
            raise Exception("call_function response does not have the expected structure")
        
        # Print the result if verbose mode is enabled
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    # No function call, just print the text response
    print(response_message.content)