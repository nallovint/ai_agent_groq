# Groq Function Calling Implementation

This project demonstrates how to implement function calling with the Groq API, using a file listing function as an example.

## Implementation Overview

The project includes:
- A `get_files_info` function that lists files in directories with security constraints
- Function schema definition for Groq API
- Main script that handles function calling and normal chat responses

## Key Deviations from Original Gemini-Based Instructions

When adapting the Gemini function calling example to work with Groq, several important changes were necessary:

### 1. **Function Schema Format**
**Original Gemini approach:**
```python
import google.genai.types as types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory...",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from..."
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
)
```

**Required Groq approach:**
```python
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in the specified directory...",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to list files from..."
                }
            }
        }
    }
}

available_functions = [schema_get_files_info]
```

### 2. **Model Selection**
**Original suggestion:** `llama-3.1-8b-instant`
**Required for function calling:** `llama3-8b-8192`

The `llama-3.1-8b-instant` model does not support function calling. Had to switch to `llama3-8b-8192` which has function calling capabilities.

### 3. **API Call Structure**
**Groq API call:**
```python
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=messages,
    tools=available_functions,  # Direct list, not wrapped in types.Tool
    tool_choice="auto"
)
```

### 4. **Function Call Handling**
**Groq response structure:**
```python
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

if tool_calls:
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        # Execute function...
```

### 5. **System Prompt Refinement**
The original system prompt needed refinement to prevent the model from attempting to call non-existent functions. Added specific guidance:

```
Only use the get_files_info function when the user specifically asks about files or directories. For other questions like math, greetings, or general queries, respond normally without calling any functions.
```

### 6. **Error Handling**
Initial implementation had issues with the model trying to call undefined functions for non-file queries. This was resolved through:
- More specific system prompt instructions
- Proper model selection
- Correct function schema format

## Usage

Run the script with various queries:

```bash
# File listing queries (triggers function calling)
uv run python main.py "list files in the current directory"
uv run python main.py "what files are in the calculator/pkg directory?"

# Non-file queries (normal responses)
uv run python main.py "what is 2 + 2?"
uv run python main.py "Hello, how are you?"
```

## Dependencies

- `groq>=0.31.0` - Groq API client
- `python-dotenv==1.1.0` - Environment variable management
- `google-genai==1.12.1` - (Note: Not actually used in final implementation)

## Project Structure

```
├── functions/
│   ├── get_files_info.py    # Function implementation and schema
│   └── ...                  # Other function modules
├── main.py                  # Main script with function calling logic
├── pyproject.toml          # Project dependencies
└── README.md               # This file
```

## Key Learnings

1. **Groq uses native Python dictionaries** for function schemas, not specialized type classes
2. **Model compatibility is crucial** - not all Groq models support function calling
3. **System prompts must be specific** about when to use functions vs. normal responses
4. **Function calling works well** but requires careful prompt engineering to avoid errors
5. **Error handling** for undefined function calls was necessary for robust operation

## Security Features

- Working directory is hardcoded for security
- Directory traversal protection in `get_files_info` function
- Relative path enforcement through function parameter design
