#!/usr/bin/env python3
"""
Manual testing script for the write_file function.
Run with: uv run tests.py
"""

from functions.write_file import write_file


def main():
    """Run manual tests for the write_file function."""
    
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


if __name__ == "__main__":
    main()
