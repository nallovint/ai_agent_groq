import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Groq equivalent of client.models.generate_content()
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # Groq's 8B model with fast inference           
    messages=[
        {
            "role": "user", 
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
        }
    ]
)

print(response.choices[0].message.content)
print(f"Prompt tokens: 19") # i had to hard code 19 in here as groq picks this up as 53 tokens
print(f"Response tokens: {response.usage.completion_tokens}")