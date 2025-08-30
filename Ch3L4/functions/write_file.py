#!/usr/bin/env python3
"""
Function to write content to files within a specified working directory.
"""

import os


def write_file(working_directory, file_path, content):
    """
    Write content to a file within the specified working directory.
    
    Args:
        working_directory (str): The permitted working directory
        file_path (str): The path to the file to write
        content (str): The content to write to the file
        
    Returns:
        str: Success message or error message
    """
    try:
        # Get absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        
        # Handle absolute vs relative file paths
        if os.path.isabs(file_path):
            # If file_path is absolute, use it as-is
            file_path_abs = os.path.abspath(file_path)
        else:
            # If file_path is relative, join it with working_directory
            file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Check if the file path is within the working directory
        if not file_path_abs.startswith(working_dir_abs + os.sep) and file_path_abs != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create directories if they don't exist
        dir_path = os.path.dirname(file_path_abs)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        # Write the content to the file
        with open(file_path_abs, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: {str(e)}'


# Function schema for Groq API
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content to a file within the working directory. Creates directories as needed.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write to, relative to the working directory."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file."
                }
            },
            "required": ["file_path", "content"]
        }
    }
}
