#!/usr/bin/env python3
"""
Manual testing script for the write_file and run_python_file functions.
Run with: uv run tests.py
"""

from functions.write_file import write_file
from functions.run_python import run_python_file


def main():
    """Run manual tests for the write_file and run_python_file functions."""
    
    print("=== Testing write_file function ===")
    
    # Test 1: Write to lorem.txt (should overwrite existing file)
    print('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):')
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"    {result1}")
    print()
    
    # Test 2: Write to a new file in pkg directory (should create file)
    print('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):')
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"    {result2}")
    print()
    
    # Test 3: Try to write to /tmp/temp.txt (should fail - outside directory)
    print('write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):')
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"    {result3}")
    print()
    
    print("=== Testing run_python_file function ===")
    
    # Test 1: Run calculator main.py (should print usage instructions)
    print('run_python_file("calculator", "main.py"):')
    result4 = run_python_file("calculator", "main.py")
    print(f"    {result4}")
    print()
    
    # Test 2: Run calculator main.py with args (should run calculator)
    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    result5 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(f"    {result5}")
    print()
    
    # Test 3: Run calculator tests.py
    print('run_python_file("calculator", "tests.py"):')
    result6 = run_python_file("calculator", "tests.py")
    print(f"    {result6}")
    print()
    
    # Test 4: Try to run file outside working directory (should fail)
    print('run_python_file("calculator", "../main.py"):')
    result7 = run_python_file("calculator", "../main.py")
    print(f"    {result7}")
    print()
    
    # Test 5: Try to run nonexistent file (should fail)
    print('run_python_file("calculator", "nonexistent.py"):')
    result8 = run_python_file("calculator", "nonexistent.py")
    print(f"    {result8}")
    print()


if __name__ == "__main__":
    main()
