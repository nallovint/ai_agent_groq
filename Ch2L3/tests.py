#!/usr/bin/env python3
"""
Manual testing script for the get_file_content function.
Run with: uv run tests.py
"""

from functions.get_file_content import get_file_content


def main():
    """Run manual tests for the get_file_content function."""
    
    # Test 1: Read lorem.txt (should truncate)
    print('get_file_content("calculator", "lorem.txt"):')
    result1 = get_file_content("calculator", "lorem.txt")
    print("Result for lorem.txt (showing first 200 chars and last 200 chars):")
    if len(result1) > 400:
        print(f"    {result1[:200]}...")
        print(f"    ...{result1[-200:]}")
    else:
        print(f"    {result1}")
    print(f"Total length: {len(result1)} characters")
    print()
    
    # Test 2: Read main.py
    print('get_file_content("calculator", "main.py"):')
    result2 = get_file_content("calculator", "main.py")
    print("Result for main.py:")
    print(result2)
    print()
    
    # Test 3: Read pkg/calculator.py
    print('get_file_content("calculator", "pkg/calculator.py"):')
    result3 = get_file_content("calculator", "pkg/calculator.py")
    print("Result for pkg/calculator.py:")
    print(result3)
    print()
    
    # Test 4: Try to access /bin/cat (should fail - outside directory)
    print('get_file_content("calculator", "/bin/cat"):')
    result4 = get_file_content("calculator", "/bin/cat")
    print("Result for /bin/cat:")
    print(f"    {result4}")
    print()
    
    # Test 5: Try to access non-existent file (should fail)
    print('get_file_content("calculator", "pkg/does_not_exist.py"):')
    result5 = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for pkg/does_not_exist.py:")
    print(f"    {result5}")


if __name__ == "__main__":
    main()
