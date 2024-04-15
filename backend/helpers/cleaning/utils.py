import re

# HELPER FUNCTIONS


def remove_long_words(text, length=15):
    # Split the text into words
    words = text.split()

    # Filter out words longer than 15 characters
    filtered_words = [word for word in words if len(word) <= length]

    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)

    return filtered_text


def remove_numbers(text):
    # Split the text into words
    words = text.split()

    # Define a regular expression pattern to match numeric characters
    numeric_pattern = re.compile(r'\d')
    underscore_pattern = re.compile(r'\b\w+_\w+\b')

    # Filter out words containing numeric characters
    filtered_words = [
        word for word in words if not numeric_pattern.search(word) and not underscore_pattern.search(word)]

    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)

    return filtered_text
