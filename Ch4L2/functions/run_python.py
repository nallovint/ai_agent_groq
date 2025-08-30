import subprocess
import os


def run_python_file(working_directory, file_path, args=[]):
    """
    Execute a Python file with specified arguments in a given working directory.
    
    Args:
        working_directory (str): The working directory to execute the file in
        file_path (str): Path to the Python file to execute
        args (list): Additional arguments to pass to the Python file
        
    Returns:
        str: Formatted output containing stdout, stderr, and any error information
    """
    try:
        # Resolve absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Check if file is outside working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        # Check if file is a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Prepare command (using uv to run Python)
        cmd = ['uv', 'run', 'python', file_path] + args
        
        # Execute the Python file
        completed_process = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Format output
        output_parts = []
        
        # Add stdout if present
        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        
        # Add stderr if present
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
        
        # Add exit code if non-zero
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        # Return formatted output or "No output produced" if empty
        if output_parts:
            return '\n'.join(output_parts)
        else:
            return "No output produced."
            
    except Exception as e:
        return f"Error executing Python file: {e}"


# Function schema for Groq API
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python file with optional arguments within the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory."
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file."
                }
            },
            "required": ["file_path"]
        }
    }
}
