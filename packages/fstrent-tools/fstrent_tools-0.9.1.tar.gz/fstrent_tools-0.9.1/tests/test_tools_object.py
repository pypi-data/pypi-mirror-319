import pytest
from src.tools_object import (
    compare_objects, get_object_attributes,
    get_object_methods, get_object_size,
    get_object_type, is_object_empty, print_obj
)

class TestClass:
    def __init__(self):
        self.attr1 = "test"
        self.attr2 = 123
    
    def method1(self):
        pass
    
    def method2(self):
        pass

@pytest.fixture
def test_object():
    return TestClass()

def test_object_attributes(test_object):
    """Test object attribute functions"""
    attrs = get_object_attributes(test_object)
    assert isinstance(attrs, dict)
    assert "attr1" in attrs
    assert "attr2" in attrs
    assert attrs["attr1"] == "test"
    assert attrs["attr2"] == 123

def test_object_methods(test_object):
    """Test object method functions"""
    methods = get_object_methods(test_object)
    assert isinstance(methods, list)
    assert "method1" in methods
    assert "method2" in methods

def test_object_comparison():
    """Test object comparison"""
    obj1 = TestClass()
    obj2 = TestClass()
    obj3 = TestClass()
    obj3.attr1 = "different"
    
    assert compare_objects(obj1, obj2) is True
    assert compare_objects(obj1, obj3) is False

def test_object_type(test_object):
    """Test object type checking"""
    assert get_object_type(test_object) == TestClass
    assert get_object_type(123) == int
    assert get_object_type("test") == str

def test_object_empty():
    """Test empty object checking"""
    assert is_object_empty("") is True
    assert is_object_empty([]) is True
    assert is_object_empty({}) is True
    assert is_object_empty("test") is False
    assert is_object_empty([1, 2, 3]) is False

def test_object_size(test_object):
    """Test object size calculation"""
    size = get_object_size(test_object)
    assert isinstance(size, int)
    assert size > 0

def test_print_obj(capsys):
    """Test object printing"""
    test_obj = TestClass()
    print_obj(test_obj)
    captured = capsys.readouterr()
    assert "TestClass" in captured.out
    assert "attr1" in captured.out
    assert "attr2" in captured.out 