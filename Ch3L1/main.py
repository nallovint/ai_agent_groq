import os
import sys
import argparse
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Hardcoded system prompt
system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

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

# Update call to use the messages list
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # Groq's 8B model with fast inference           
    messages=messages,
)

# Output based on verbose flag
if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

print(response.choices[0].message.content)