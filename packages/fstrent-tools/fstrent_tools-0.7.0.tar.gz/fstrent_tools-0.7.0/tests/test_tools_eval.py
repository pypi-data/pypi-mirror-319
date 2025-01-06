import pytest
from src.tools_eval import (
    AllHaveVal, HasVal, is_even, is_odd,
    is_valid_email, is_valid_path
)

def test_value_validation():
    """Test value validation functions"""
    assert HasVal("test") is True
    assert HasVal("") is False
    assert HasVal(None) is False
    
    values = ["test", 123, True]
    assert AllHaveVal(values) is True
    
    values_with_empty = ["test", "", None]
    assert AllHaveVal(values_with_empty) is False

def test_number_checks():
    """Test number validation functions"""
    assert is_even(2) is True
    assert is_even(3) is False
    assert is_odd(3) is True
    assert is_odd(2) is False

def test_format_validation():
    """Test format validation functions"""
    assert is_valid_email("test@example.com") is True
    assert is_valid_email("invalid-email") is False
    
    assert is_valid_path("/valid/path") is True
    assert is_valid_path("invalid:path") is False 