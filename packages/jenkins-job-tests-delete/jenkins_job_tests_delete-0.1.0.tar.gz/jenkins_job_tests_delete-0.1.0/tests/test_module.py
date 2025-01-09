import pytest
from src.module import some_function, custom_display, calculate_sum, filter_positive, reverse_string

def test_some_function():
    result = some_function()
    print("Running test_some_function:")
    print(f"  Input: None")
    print(f"  Expected Output: 'Hello, world!'")
    print(f"  Actual Output: {result}")
    assert result == "Hello, world!"

def test_custom_display():
    result_default = custom_display("Hello")
    result_warn = custom_display("Warning!", prefix="WARN")
    print("\nRunning test_custom_display:")
    print(f"  Input: ('Hello', default prefix)")
    print(f"  Expected Output: '[INFO] Hello'")
    print(f"  Actual Output: {result_default}")
    assert result_default == "[INFO] Hello"

    print(f"  Input: ('Warning!', prefix='WARN')")
    print(f"  Expected Output: '[WARN] Warning!'")
    print(f"  Actual Output: {result_warn}")
    assert result_warn == "[WARN] Warning!"

def test_calculate_sum():
    numbers = [1, 2, 3, 4]
    result = calculate_sum(numbers)
    print("\nRunning test_calculate_sum:")
    print(f"  Input: {numbers}")
    print(f"  Expected Output: 10")
    print(f"  Actual Output: {result}")
    assert result == 10

def test_filter_positive():
    numbers = [1, -2, 3, -4, 0]
    result = filter_positive(numbers)
    print("\nRunning test_filter_positive:")
    print(f"  Input: {numbers}")
    print(f"  Expected Output: [1, 3]")
    print(f"  Actual Output: {result}")
    assert result == [1, 3]

def test_reverse_string():
    input_string = "hello"
    result = reverse_string(input_string)
    print("\nRunning test_reverse_string:")
    print(f"  Input: '{input_string}'")
    print(f"  Expected Output: 'olleh'")
    print(f"  Actual Output: {result}")
    assert result == "olleh"
