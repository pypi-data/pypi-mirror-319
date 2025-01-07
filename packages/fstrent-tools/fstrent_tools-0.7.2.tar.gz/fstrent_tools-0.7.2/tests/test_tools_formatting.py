import pytest
from src.tools_formatting import (
    format_dict, format_list, format_table,
    indent_text, print_adv, print_func_name,
    print_line, print_obj
)

def test_format_dict():
    """Test dictionary formatting"""
    test_dict = {"a": 1, "b": 2}
    formatted = format_dict(test_dict)
    assert isinstance(formatted, str)
    assert "a" in formatted
    assert "b" in formatted

def test_format_list():
    """Test list formatting"""
    test_list = ["item1", "item2"]
    formatted = format_list(test_list)
    assert isinstance(formatted, str)
    assert "item1" in formatted
    assert "item2" in formatted

def test_format_table():
    """Test table formatting"""
    headers = ["Name", "Age"]
    data = [["John", "30"], ["Jane", "25"]]
    formatted = format_table(data, headers)
    assert isinstance(formatted, str)
    assert "Name" in formatted
    assert "Age" in formatted

def test_indent_text():
    """Test text indentation"""
    text = "Test\nText"
    indented = indent_text(text, spaces=4)
    assert indented.startswith("    Test")
    assert "\n    Text" in indented 