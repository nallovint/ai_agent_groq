# Deviations from Original Gemini Implementation

This document outlines the key deviations and changes required to translate the original Gemini-based function calling implementation to work with Groq's API.

## Major API Structure Changes

### 1. Model Selection
**Original Request**: Use Gemini's `generate_content` method
**Deviation**: Had to use Groq's `client.chat.completions.create` method with specific model selection

- **Initial attempt**: `llama3-8b-8192` - worked but had inconsistent function calling behavior
- **Failed attempt**: `llama3-groq-70b-8192-tool-use-preview` - model was decommissioned
- **Final working solution**: `llama3-70b-8192` - provided reliable function calling

### 2. Response Structure Handling
**Original Request**: Check `.candidates` property and iterate over candidates
**Deviation**: Groq responses use a different structure:

```python
# Original Gemini approach (from request):
# response.candidates property with iterations over each candidate
# candidate.content to add to messages

# Groq implementation:
response_message = response.choices[0].message
# Add entire response_message to conversation
messages.append({
    "role": "assistant", 
    "content": response_message.content,
    "tool_calls": response_message.tool_calls
})
```

### 3. Function Response Conversion
**Original Request**: Use `types.Content` function to convert function responses
**Deviation**: Had to create custom message structure for Groq:

```python
# Instead of types.Content function, use:
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "name": function_name, 
    "content": json.dumps(function_call_result.parts[0].function_response.response)
})
```

## System Prompt Modifications

### 1. Initial System Prompt Issues
**Original**: Basic function usage instructions
**Problem**: LLM was making inappropriate function calls (like `write_file` with empty content)
**Solution**: Had to significantly enhance the system prompt with:

- Specific guidance on when to use functions vs. normal responses
- Clear instructions about the calculator project context
- Explicit directions to explore files when asked about code functionality

### 2. Function Call Format Issues
**Problem**: LLM attempted to use XML-style tool calling format instead of native Groq function calling
**Solution**: Added explicit instruction: "Use normal function calling - do not use any XML tags or special formatting for function calls"

### 3. Function Call Ordering Issues
**Problem**: AI was calling `get_file_content` directly without first exploring directory structure
**Test Requirement**: Expected stdout to contain both 'get_files_info' and 'get_file_content'
**Solution**: Added explicit step-by-step instructions with "ALWAYS start by calling get_files_info"

### 4. Final Working System Prompt
```python
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
```

## Loop Implementation Changes

### 1. Termination Condition
**Original Request**: Check for `response.text` property
**Deviation**: Groq responses don't have a `.text` property
**Solution**: Check `response_message.content` instead:

```python
if response_message.content:
    print("Final response:")
    print(response_message.content)
    break
```

### 2. Tool Call Processing
**Original Request**: Use Gemini's tool call structure
**Deviation**: Had to adapt to Groq's tool call format:

```python
# Groq format:
tool_calls = response_message.tool_calls
if tool_calls:
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
```

## Error Handling Additions

Added comprehensive error handling that wasn't explicitly requested:
- Try-catch wrapper around entire conversation loop
- Graceful handling of decommissioned models
- Protection against infinite loops with multiple exit conditions
- Verbose error reporting with stack traces when requested

## Testing Challenges

### 1. Function Call Reliability
**Issue**: Initial models and prompts led to inconsistent function calling behavior
**Solution**: Required multiple iterations of:
- Model selection (3 different models tried)
- System prompt refinement (4 major revisions)
- Response handling adjustments

### 2. Expected vs. Actual Behavior
**Expected**: AI should call `get_files_info`, then `get_file_content` on relevant files
**Initial Result**: AI called inappropriate functions or used wrong calling format
**Final Result**: AI correctly explores directory structure and reads relevant files

## Calculator Bug Fix Task Deviations

### Issue with Initial Bug Report Prompting
**Task**: Ask the agent to fix a precedence bug in the calculator where "3 + 7 * 2 shouldn't be 20"

**Initial Approach**: Used a generic bug report: "fix the bug: 3 + 7 * 2 shouldn't be 20"
**Problem**: The agent identified the issue but only provided code suggestions without actually implementing the fix

**Required Deviation**: Had to change the prompting strategy to be more explicit:
- **First attempt**: Generic bug description - agent explained the problem but didn't fix it
- **Second attempt**: More specific request: "The calculator precedence is wrong. In calculator/pkg/calculator.py, the + operator has precedence 3 but it should be 1. Please fix this by updating the precedence values." - agent showed correct code but still didn't implement
- **Final working approach**: Direct function instruction: "Please use the write_file function to fix calculator/pkg/calculator.py by changing the precedence of + from 3 back to 1"

### Key Learning
When asking Groq agents to fix code issues, generic bug reports may not trigger the agent to use its file modification functions. Instead, explicit instructions to use specific functions (like `write_file`) are often necessary to get the agent to actually implement fixes rather than just suggest them.

This suggests that Groq models may need more explicit prompting about when to take action versus when to just provide analysis, compared to what might be expected from other AI systems.

## Summary of Required Changes

To make this work with Groq instead of Gemini, the following major changes were essential:

1. **Complete API structure rewrite** - Groq and Gemini have fundamentally different response formats
2. **Model-specific optimizations** - Required finding the right Groq model that supports reliable function calling
3. **Extensive system prompt engineering** - Much more detailed instructions needed than originally specified
4. **Custom message formatting** - Had to create Groq-compatible message structures for tool responses
5. **Enhanced error handling** - Added robustness not specified in original requirements
6. **More explicit action prompting** - Groq agents may need direct instructions to use modification functions rather than just analyze code

The core conversation loop concept from the original request worked well, but nearly every implementation detail had to be adapted for Groq's different API structure and behavior patterns.
