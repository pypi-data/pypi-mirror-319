import pytest
from src import tools_convert, tools_strings, tools_dicts

def test_string_operations():
    """Test basic string manipulation functions"""
    from src.tools_strings import left, right, mid, pad_string
    
    # Test left/right/mid
    assert left("hello", 2) == "he"
    assert right("hello", 2) == "lo"
    assert mid("hello", 1, 3) == "ell"
    
    # Test padding
    assert pad_string("test", 8) == "test    "

def test_conversions():
    """Test type conversion functions"""
    from src.tools_convert import convert_2_boolean, convert_2_float
    
    assert convert_2_boolean("true") is True
    assert convert_2_boolean("0") is False
    assert convert_2_float("123.45") == 123.45

def test_dict_operations():
    """Test dictionary utility functions"""
    from src.tools_dicts import DictKeyVal, DictContainsKeys
    
    test_dict = {"a": 1, "b": 2}
    assert DictKeyVal(test_dict, "a") is True
    assert DictContainsKeys(test_dict, ["a", "b"]) is True 