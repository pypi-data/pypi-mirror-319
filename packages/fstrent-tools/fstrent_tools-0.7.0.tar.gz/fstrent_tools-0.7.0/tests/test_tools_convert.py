import pytest
from decimal import Decimal
from src.tools_convert import (
    convert_2_boolean, convert_2_dict, convert_2_float,
    convert_2_integer, convert_2_list, convert_2_string,
    dec, dec_2_float, dec_prec, dict_2_obj, tf, tf_2_int
)

def test_boolean_conversions():
    """Test boolean conversion functions"""
    assert convert_2_boolean("true") is True
    assert convert_2_boolean("false") is False
    assert convert_2_boolean(1) is True
    assert convert_2_boolean(0) is False
    
    assert tf("TRUE") is True
    assert tf("FALSE") is False
    assert tf_2_int(True) == 1
    assert tf_2_int(False) == 0

def test_numeric_conversions():
    """Test numeric conversion functions"""
    assert convert_2_float("123.45") == 123.45
    assert convert_2_integer("123") == 123
    assert isinstance(dec("123.45"), Decimal)
    assert dec_2_float(Decimal("123.45")) == 123.45
    assert dec_prec(Decimal("123.456789"), 2) == 123.46

def test_collection_conversions():
    """Test collection conversion functions"""
    assert convert_2_list("a,b,c") == ["a", "b", "c"]
    assert convert_2_dict('{"a": 1}') == {"a": 1}
    
    class TestObj:
        pass
    
    obj = dict_2_obj({"a": 1, "b": 2}, TestObj())
    assert obj.a == 1
    assert obj.b == 2 