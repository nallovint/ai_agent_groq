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
You are a helpful AI coding agent working with a calculator project.

You have access to the following functions which you can call to explore the codebase:
- get_files_info: Lists files in the specified directory along with their sizes
- get_file_content: Read the contents of a file within the working directory  
- run_python_file: Execute Python files with optional arguments
- write_file: Write or overwrite files

When a user asks about how code works, what files do, or wants to understand the implementation:
1. ALWAYS start by calling get_files_info to explore the directory structure
2. Then use get_file_content to read relevant source files based on what you found
3. Analyze the code and explain how it works

The working directory is set to "./calculator" which contains the calculator project files.

Use normal function calling - do not use any XML tags or special formatting for function calls. Just call the functions directly when you need to examine files or understand how the code works.

All file paths should be relative to the working directory.
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

# Create conversation loop to handle multiple rounds of tool use
max_iterations = 20
iteration_count = 0

# Output initial information if verbose
if verbose:
    print(f"User prompt: {user_prompt}")

try:
    while iteration_count < max_iterations:
        iteration_count += 1
        
        # Make API call with current messages
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Groq's 70B model with function calling support         
            messages=messages,
            tools=available_functions,
            tool_choice="auto"
        )
        
        # Output token usage if verbose
        if verbose:
            print(f"Iteration {iteration_count} - Prompt tokens: {response.usage.prompt_tokens}, Response tokens: {response.usage.completion_tokens}")
        
        # Get the response message
        response_message = response.choices[0].message
        
        # Add the assistant's response to the conversation
        messages.append({
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": response_message.tool_calls if response_message.tool_calls else None
        })
        
        # Check if the LLM called any functions
        tool_calls = response_message.tool_calls
        
        if tool_calls:
            # Handle each function call
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
                
                # Add the function result as a tool message to the conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(function_call_result.parts[0].function_response.response)
                })
                
                # Print the result if verbose mode is enabled
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # Continue the loop to get the LLM's response to the function results
            continue
        
        # If no tool calls and we have a text response, we're done
        if response_message.content:
            print("Final response:")
            print(response_message.content)
            break
        
        # If we somehow get here without content or tool calls, break to avoid infinite loop
        if not response_message.content and not tool_calls:
            print("No response content or tool calls. Ending conversation.")
            break
    
    if iteration_count >= max_iterations:
        print(f"Reached maximum iterations ({max_iterations}). Ending conversation.")

except Exception as e:
    print(f"Error during conversation: {str(e)}")
    if verbose:
        import traceback
        traceback.print_exc()