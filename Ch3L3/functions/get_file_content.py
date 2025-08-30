"""Function to safely read file contents with security checks and truncation."""

import os
from pathlib import Path
from .config import MAX_FILE_CHARACTERS


def get_file_content(working_directory, file_path):
    """
    Read file content with security checks and truncation.
    
    Args:
        working_directory (str): The base working directory
        file_path (str): Path to the file to read (relative to working_directory or absolute)
    
    Returns:
        str: File contents (truncated if > MAX_FILE_CHARACTERS) or error message
    """
    try:
        # Convert to Path objects for easier manipulation
        working_dir = Path(working_directory).resolve()
        
        # Handle absolute vs relative paths
        if os.path.isabs(file_path):
            target_path = Path(file_path).resolve()
        else:
            target_path = (working_dir / file_path).resolve()
        
        # Security check: ensure target_path is within working_directory
        try:
            target_path.relative_to(working_dir)
        except ValueError:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists and is a regular file
        if not target_path.exists() or not target_path.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Truncate if necessary
        if len(content) > MAX_FILE_CHARACTERS:
            content = content[:MAX_FILE_CHARACTERS]
            content += f'[...File "{file_path}" truncated at {MAX_FILE_CHARACTERS} characters]'
        
        return content
        
    except Exception as e:
        return f"Error: {str(e)}"


# Function schema for Groq API
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read the contents of a file within the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory."
                }
            },
            "required": ["file_path"]
        }
    }
}
