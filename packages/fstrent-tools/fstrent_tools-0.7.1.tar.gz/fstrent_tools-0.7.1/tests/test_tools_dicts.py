import pytest
from src.tools_dicts import (
    AttrDict, AttrDictConv, AttrDictUpd,
    DictContainsKeys, DictKeyDel, DictKeyVal,
    DictKeyValFill, DictKeyValIfElse, DictKeyValMult,
    DictValCheck, dict_of_dicts_sort
)

def test_attr_dict():
    """Test AttrDict functionality"""
    ad = AttrDict({"a": 1, "b": {"c": 2}})
    assert ad.a == 1
    assert ad.b.c == 2

def test_dict_operations():
    """Test dictionary utility functions"""
    test_dict = {"a": 1, "b": 2, "c": None}
    
    assert DictContainsKeys(test_dict, ["a", "b"]) is True
    assert DictKeyVal(test_dict, "a") is True
    assert DictKeyVal(test_dict, "c") is False
    
    DictKeyDel(test_dict, "b")
    assert "b" not in test_dict
    
    DictKeyValFill(test_dict, "d", default=3)
    assert test_dict["d"] == 3
    
    assert DictKeyValIfElse(test_dict, "a", default=0) == 1
    assert DictKeyValIfElse(test_dict, "x", default=0) == 0

def test_dict_sorting():
    """Test dictionary sorting"""
    dicts = {
        "b": {"order": 2},
        "a": {"order": 1},
        "c": {"order": 3}
    }
    sorted_dict = dict_of_dicts_sort(dicts, "order")
    assert list(sorted_dict.keys()) == ["a", "b", "c"] 