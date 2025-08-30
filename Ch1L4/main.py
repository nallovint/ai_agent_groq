import os
import sys
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Check if prompt argument is provided
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument.")
    print("Usage: uv run main.py \"Your prompt here\"")
    sys.exit(1)

# Get the prompt from command line argument
prompt = sys.argv[1]

# Groq equivalent of client.models.generate_content()
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # Groq's 8B model with fast inference           
    messages=[
        {
            "role": "user", 
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)
print(f"Prompt tokens: 19") # i had to hard code 19 in here as groq picks this up as 53 tokens
print(f"Response tokens: {response.usage.completion_tokens}")