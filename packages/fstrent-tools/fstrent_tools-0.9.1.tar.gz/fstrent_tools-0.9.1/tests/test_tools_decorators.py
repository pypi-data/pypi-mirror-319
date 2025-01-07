import pytest
from src.tools_decorators import debug_class, timing_class, singleton

def test_singleton_decorator():
    """Test singleton decorator"""
    @singleton
    class TestClass:
        pass
    
    instance1 = TestClass()
    instance2 = TestClass()
    assert instance1 is instance2

@pytest.mark.parametrize("decorator", [
    debug_class,
    timing_class
])
def test_class_decorators(decorator):
    """Test class decorators"""
    @decorator
    class TestClass:
        def test_method(self):
            return "test"
    
    obj = TestClass()
    assert obj.test_method() == "test" 