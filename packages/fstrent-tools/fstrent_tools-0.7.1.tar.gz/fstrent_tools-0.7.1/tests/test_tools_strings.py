import pytest
from src.tools_strings import (
    IsEnglish, camel_to_snake, snake_to_camel,
    cpad, lpad, rpad, left, mid, right,
    display_length, extract_numbers, remove_special_chars
)

def test_case_conversions():
    """Test case conversion functions"""
    assert camel_to_snake("helloWorld") == "hello_world"
    assert snake_to_camel("hello_world") == "helloWorld"

def test_padding():
    """Test string padding functions"""
    assert lpad("test", 8) == "    test"
    assert rpad("test", 8) == "test    "
    assert cpad("test", 8) == "  test  "

def test_substring():
    """Test substring functions"""
    text = "Hello World"
    assert left(text, 5) == "Hello"
    assert right(text, 5) == "World"
    assert mid(text, 6, 5) == "World"

def test_string_utilities():
    """Test utility functions"""
    assert IsEnglish("Hello") is True
    assert IsEnglish("こんにちは") is False
    assert extract_numbers("abc123def456") == "123456"
    assert remove_special_chars("Hello@World!") == "HelloWorld" 