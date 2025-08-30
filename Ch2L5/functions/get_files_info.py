import os


def get_files_info(working_directory, directory="."):
    """
    Get information about files and directories within a restricted working directory.
    
    Args:
        working_directory: The base directory that limits file access
        directory: Relative path within the working_directory to list (default: ".")
    
    Returns:
        String with formatted file information or error message
    """
    try:
        # Create the full path by joining working_directory and directory
        full_path = os.path.join(working_directory, directory)
        
        # Get the absolute path and normalize it
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)
        
        # Security check: ensure the target directory is within working_directory
        if not abs_full_path.startswith(abs_working_dir + os.sep) and abs_full_path != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the path exists and is a directory
        if not os.path.exists(abs_full_path):
            return f'Error: "{directory}" does not exist'
        
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'
        
        # List directory contents
        items = []
        for item_name in sorted(os.listdir(abs_full_path)):
            item_path = os.path.join(abs_full_path, item_name)
            
            # Get file size and check if it's a directory
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            
            items.append(f" - {item_name}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(items)
    
    except Exception as e:
        return f"Error: {str(e)}"
