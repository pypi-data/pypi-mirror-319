import pytest
from src.tools_debug import debug_print, print_stack, print_traceback
from contextlib import redirect_stdout
import io

def test_debug_print():
    """Test debug print functionality"""
    output = io.StringIO()
    with redirect_stdout(output):
        debug_print("test message", level=1)
    assert "test message" in output.getvalue()

def test_stack_trace():
    """Test stack trace printing"""
    output = io.StringIO()
    with redirect_stdout(output):
        print_stack()
    assert "File" in output.getvalue() 