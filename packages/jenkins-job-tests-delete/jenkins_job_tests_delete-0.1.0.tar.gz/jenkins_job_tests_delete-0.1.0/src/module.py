# src/module.py

def some_function():
    """Basic function that returns a greeting."""
    return "Hello, world!"

def custom_display(message, prefix="INFO"):
    """Displays a formatted message with a custom prefix."""
    return f"[{prefix}] {message}"

def calculate_sum(numbers):
    """Calculates the sum of a list of numbers."""
    return sum(numbers)

def filter_positive(numbers):
    """Filters and returns only positive numbers from a list."""
    return [n for n in numbers if n > 0]

def reverse_string(input_string):
    """Reverses the given string."""
    return input_string[::-1]
